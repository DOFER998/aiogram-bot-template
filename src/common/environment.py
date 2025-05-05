from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Bot(BaseModel):
    token: SecretStr


class Server(BaseModel):
    port: int
    host: str
    webhook_url: str
    secret_token: SecretStr


class Environment(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_ignore_empty=True,
        env_file_encoding='utf-8',
        env_nested_delimiter='__',
    )

    bot: Bot
    server: Server


env = Environment()
