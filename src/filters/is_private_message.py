from aiogram.enums import ChatType
from aiogram.filters import Filter
from aiogram.types import Message


class IsPrivateMessageFilter(Filter):
    def __init__(self) -> None:
        self.chat_type = ChatType

    async def __call__(self, msg: Message) -> bool:
        return msg.chat.type == self.chat_type.PRIVATE
