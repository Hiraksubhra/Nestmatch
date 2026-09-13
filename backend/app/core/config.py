from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    APP_ENV: str = "development"
    PROJECT_NAME: str = "NestMatch API"
    VERSION: str = "0.1.0"
    SECRET_KEY: str = "e839e94474775d0a6bb81efca3b069d25a81615f3813a846c2faea7e9f3b1402"
    ALGORITHM: str = "HS256"
    ALLOWED_ORIGINS: Union[List[str], str] = "http://localhost:5173,http://127.0.0.1:5173,https://nestmatch.vercel.app"

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./nestmatch.db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Third Party Integrations
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""
    SENDGRID_API_KEY: str = ""
    FROM_EMAIL: str = "noreply@nestmatch.in"
    FRONTEND_URL: str = "http://localhost:5173"

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",") if i.strip()]
        return v


settings = Settings()
