import os
from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding='utf-8')
    API_TELEGRAM: str
    PAYMENT_TOKEN: str
    WEBHOOK_URI: str
    SERV_HOST: str
    SERV_PORT: int


settings = Settings()
