from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union

class Settings(BaseSettings):
    database_url: str
    cors_origins: Union[str, List[str]] = ["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173"]
    environment: str = "development"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
