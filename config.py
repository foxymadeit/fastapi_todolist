from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
import os



class Settings(BaseSettings):

    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    SECRET_KEY: SecretStr
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    model_config = SettingsConfigDict(env_file=os.getenv("ENV_FILE", ".env"))


settings = Settings()
