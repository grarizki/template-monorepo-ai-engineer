from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "ai-template"
    VERSION: str = "0.1.0"
    database_url: str = "sqlite:///./db.sqlite"


settings = Settings()
