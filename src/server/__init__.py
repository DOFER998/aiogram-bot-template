import asyncio
import secrets
from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable, Dict, Optional, Tuple

from aiogram import Bot, Dispatcher, loggers
from aiogram.methods import TelegramMethod
from aiogram.methods.base import TelegramType
from aiogram.types import InputFile
from aiogram.webhook.security import IPFilter
from aiohttp import MultipartWriter
from fastapi import FastAPI, Request, Response, HTTPException, status
from starlette.responses import JSONResponse


def setup_application(app: FastAPI, dispatcher: Dispatcher, /, **kwargs: Any) -> None:
    """
    This function helps to configure a startup-shutdown process

    :param app: fastapi application
    :param dispatcher: aiogram dispatcher
    :param kwargs: additional data
    :return:
    """
    workflow_data = {
        'app': app,
        'dispatcher': dispatcher,
        **dispatcher.workflow_data,
        **kwargs,
    }

    async def on_startup(*a: Any, **kw: Any) -> None:  # pragma: no cover
        await dispatcher.emit_startup(**workflow_data)

    async def on_shutdown(*a: Any, **kw: Any) -> None:  # pragma: no cover
        await dispatcher.emit_shutdown(**workflow_data)

    app.add_event_handler('startup', on_startup)
    app.add_event_handler('shutdown', on_shutdown)


def check_ip(ip_filter: IPFilter, request: Request) -> Tuple[str, bool]:
    # Try to resolve client IP over reverse proxy
    if forwarded_for := request.headers.get('X-Forwarded-For', ''):
        # Get the left-most ip when there is multiple ips
        # (request got through multiple proxy/load balancers)
        # https://github.com/aiogram/aiogram/issues/672
        forwarded_for, *_ = forwarded_for.split(',', maxsplit=1)
        return forwarded_for, forwarded_for in ip_filter

    # When reverse proxy is not configured IP address can be resolved from incoming connection
    if peer_name := request.client.host:
        host, _ = peer_name
        return host, host in ip_filter

    # Potentially impossible case
    return '', False  # pragma: no cover


def ip_filter_middleware(
        ip_filter: IPFilter,
) -> Callable[[Request, Any], Awaitable[Any]]:
    """

    :param ip_filter:
    :return:
    """

    async def _ip_filter_middleware(request: Request, handler) -> Any:
        ip_address, accept = check_ip(ip_filter=ip_filter, request=request)
        if not accept:
            loggers.webhook.warning(f'Blocking request from an unauthorized IP: {ip_address}')
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return await handler(request)

    return _ip_filter_middleware


class BaseRequestHandler(ABC):
    def __init__(
            self, dispatcher: Dispatcher, handle_in_background: bool = True, **data: Any
    ) -> None:
        """
        Base handler that helps to handle incoming request from aiohttp
        and propagate it to the Dispatcher

        :param dispatcher: instance of :class:`aiogram.dispatcher.dispatcher.Dispatcher`
        :param handle_in_background: immediately responds to the Telegram instead of
            a waiting end of a handler process
        """
        self.dispatcher = dispatcher
        self.handle_in_background = handle_in_background
        self.data = data

    def register(self, app: FastAPI, /, path: str, **kwargs: Any) -> None:
        """
        Register route and shutdown callback

        :param app: instance of aiohttp Application
        :param path: route path
        :param kwargs:
        """
        app.add_event_handler('shutdown', self._handle_close)
        app.add_route(path=path, route=self.handle, methods=['POST'])

    async def _handle_close(self) -> None:
        await self.close()

    @abstractmethod
    async def close(self) -> None:
        pass

    @abstractmethod
    async def resolve_bot(self, request: Request) -> Bot:
        """
        This method should be implemented in subclasses of this class.

        Resolve Bot instance from request.

        :param request:
        :return: Bot instance
        """
        pass

    @abstractmethod
    def verify_secret(self, telegram_secret_token: str, bot: Bot) -> bool:
        pass

    async def _background_feed_update(self, bot: Bot, update: Dict[str, Any]) -> None:
        result = await self.dispatcher.feed_raw_update(bot=bot, update=update, **self.data)
        if isinstance(result, TelegramMethod):
            await self.dispatcher.silent_call_request(bot=bot, result=result)

    async def _handle_request_background(self, bot: Bot, request: Request) -> Response:
        asyncio.create_task(
            self._background_feed_update(
                bot=bot, update=bot.session.json_loads(await request.body())
            )
        )
        return Response(bot.session.json_dumps({}), media_type='application/json')

    def _build_response_writer(
            self, bot: Bot, result: Optional[TelegramMethod[TelegramType]]
    ) -> MultipartWriter:
        writer = MultipartWriter(
            'form-data',
            boundary=f'webhookBoundary{secrets.token_urlsafe(16)}',
        )
        if not result:
            return writer

        payload = writer.append(result.__api_method__)
        payload.set_content_disposition('form-data', name='method')

        files: Dict[str, InputFile] = {}
        for key, value in result.model_dump(warnings=False).items():
            value = bot.session.prepare_value(value, bot=bot, files=files)
            if not value:
                continue
            payload = writer.append(value)
            payload.set_content_disposition('form-data', name=key)

        for key, value in files.items():
            payload = writer.append(value.read(bot))
            payload.set_content_disposition(
                'form-data',
                name=key,
                filename=value.filename or key,
            )

        return writer

    async def _handle_request(self, bot: Bot, request: Request) -> Response:
        result: Optional[TelegramMethod[Any]] = await self.dispatcher.feed_webhook_update(
            bot,
            bot.session.json_loads(await request.body()),
            **self.data,
        )
        response = self._build_response_writer(bot=bot, result=result)

        return Response(
            content=response._value,
            headers=response.headers,
            media_type=response.content_type,
        )

    async def handle(self, request: Request) -> Response:
        bot = await self.resolve_bot(request)

        if not self.verify_secret(request.headers.get('X-Telegram-Bot-Api-Secret-Token', ''), bot):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={'message': 'Unauthorized.'},
            )

        if self.handle_in_background:
            return await self._handle_request_background(bot=bot, request=request)
        return await self._handle_request(bot=bot, request=request)

    __call__ = handle


class SimpleRequestHandler(BaseRequestHandler):
    def __init__(
            self,
            dispatcher: Dispatcher,
            bot: Bot,
            handle_in_background: bool = True,
            secret_token: Optional[str] = None,
            **data: Any,
    ) -> None:
        """
        Handler for single Bot instance

        :param dispatcher: instance of :class:`aiogram.dispatcher.dispatcher.Dispatcher`
        :param handle_in_background: immediately responds to the Telegram instead of
            a waiting end of handler process
        :param bot: instance of :class:`aiogram.client.bot.Bot`
        """
        super().__init__(dispatcher=dispatcher, handle_in_background=handle_in_background, **data)
        self.bot = bot
        self.secret_token = secret_token

    def verify_secret(self, telegram_secret_token: str, bot: Bot) -> bool:
        if self.secret_token:
            return secrets.compare_digest(telegram_secret_token, self.secret_token)
        return True

    async def close(self) -> None:
        """
        Close bot session
        """
        await self.bot.session.close()

    async def resolve_bot(self, request: Request) -> Bot:
        return self.bot
