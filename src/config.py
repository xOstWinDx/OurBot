from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    BOT_TOKEN: str
    TELEGRAM_USER_IDS: list

    model_config = SettingsConfigDict(env_file=".env")


config = Config()
