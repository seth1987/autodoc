"""Configuration module for AutoDoc."""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # App settings
    app_name: str = "AutoDoc"
    debug: bool = False

    # CORS settings
    cors_origins: str = "*"

    # File upload settings
    max_file_size_mb: int = 50
    allowed_extensions: str = "pdf,docx"

    # LLM settings
    default_llm_provider: str = "openai"
    chunking_threshold: int = 6000

    # Timeouts
    llm_timeout_seconds: int = 120

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
