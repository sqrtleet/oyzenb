from os import getenv
from datetime import timedelta

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    class Config:
        env_file = ".env"


settings = Settings()

POSTGRES_URL = "postgresql://{}:{}@{}:{}/{}".format(
    settings.POSTGRES_USER,
    settings.POSTGRES_PASSWORD,
    settings.POSTGRES_HOST,
    settings.POSTGRES_PORT,
    settings.POSTGRES_DB,
)
jwt_secret_key = getenv("JWT_SECRET_KEY")
jwt_algorithm = "HS256"
jwt_token_lifetime = timedelta(days=1)
