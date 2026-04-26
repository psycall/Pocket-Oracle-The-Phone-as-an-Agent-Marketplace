"""
Orvion — Core Configuration
All secrets come from environment variables. Never hardcode.
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # ── Node Identity ────────────────────────────────────────
    NODE_ID: str = "orvion-node-001"
    NODE_TYPE: str = "execution"
    ENVIRONMENT: str = "development"

    # ── Security ─────────────────────────────────────────────
    SECRET_KEY: str                    # Required — set in .env
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24  # 24h

    # ── LLM (Anthropic) ──────────────────────────────────────
    ANTHROPIC_API_KEY: str             # Required — set in .env
    ANTHROPIC_MODEL: str = "claude-opus-4-5"
    ANTHROPIC_MAX_TOKENS: int = 1024

    # ── Database ─────────────────────────────────────────────
    DATABASE_URL: str = "sqlite:///./orvion.db"
    REDIS_URL: str = "redis://localhost:6379"

    # ── CORS ─────────────────────────────────────────────────
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "https://orvion.dev"]

    # ── Rate Limiting ─────────────────────────────────────────
    RATE_LIMIT_PER_MINUTE: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
