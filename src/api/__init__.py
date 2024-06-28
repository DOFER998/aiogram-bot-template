from aiogram.exceptions import TelegramBadRequest
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .routers import root_router, webhook_router

app = FastAPI()

app.include_router(root_router)
app.include_router(webhook_router)


@app.exception_handler(TelegramBadRequest)
async def error_handler(_request: Request, exc: TelegramBadRequest):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({'error': str(exc)}),
    )


__all__ = [
    'app',
]
