from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class EnvironmentVariables(BaseSettings):
    TG_BOT_API_TOKEN: str
    TG_WEBHOOK_TOKEN: str

    model_config = SettingsConfigDict(env_file=".env")


env = EnvironmentVariables()
