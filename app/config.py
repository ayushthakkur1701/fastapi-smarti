# app/config.py

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    database_hostname: str = Field(..., env='DATABASE_HOSTNAME')
    database_username: str = Field(..., env='DATABASE_USERNAME')
    database_password: str = Field(..., env='DATABASE_PASSWORD')
    database_port: str = Field(..., env='DATABASE_PORT')
    database_name: str = Field(..., env='DATABASE_NAME')
    secret_key: str = Field(..., env='SECRET_KEY')
    algorithm: str = Field(..., env='ALGORITHM')
    access_token_expire_minutes: int = Field(..., env='ACCESS_TOKEN_EXPIRE_MINUTES')

    class Config:
        env_file = '.env'  # Specify the .env file to load

# Instantiate the settings
settings = Settings()