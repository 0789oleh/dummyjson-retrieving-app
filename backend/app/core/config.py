import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv('DATABASE_URL')
    PROJECT_NAME: str = "DummyJSON API Backend"


settings = Settings()
