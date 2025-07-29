# src/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # A URL agora inclui as credenciais
    DATABASE_URL: str = Field(default="mongodb://root:rootpassword@localhost:27017/store_db")
    DB_NAME: str = Field(default="store_db")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")