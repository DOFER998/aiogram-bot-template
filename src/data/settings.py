from typing import Dict

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    token: str = None
    rate_limit: float = None
    webhook_url: str = None
    api_id: int = None
    api_hash: str = None
    redis_host: str = None
    redis_port: int = None
    redis_db: int = None
    telegram_bot_api_url: str = None


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)


class UserCommands(BaseSettings):
    commands: Dict[str, str] = {
        'start': '💼 Главное меню',
    }


user_commands = UserCommands()
