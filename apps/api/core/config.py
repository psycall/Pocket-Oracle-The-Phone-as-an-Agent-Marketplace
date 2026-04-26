"""
Orvion — Core Configuration
All secrets come from environment variables. Never hardcode.
Designed so demos still work when optional providers are unavailable.
"""

from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ── Node Identity ────────────────────────────────────────
    NODE_ID: str = "orvion-node-001"
    NODE_TYPE: str = "execution"
    ENVIRONMENT: str = "development"

    # ── Security ─────────────────────────────────────────────
    SECRET_KEY: str = "change-me-before-production-32+chars"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24

    # ── LLM (Anthropic) — optional in demo mode ──────────────
    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-3-5-sonnet-latest"
    ANTHROPIC_MAX_TOKENS: int = 1024
    DEMO_MODE: bool = True

    # ── Database ─────────────────────────────────────────────
    DATABASE_URL: str = "sqlite:///./orvion.db"
    REDIS_URL: str = "redis://localhost:6379"

    # ── CORS ─────────────────────────────────────────────────
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:8080",
        "https://orvion.dev",
    ]

    # ── Rate Limiting ─────────────────────────────────────────
    RATE_LIMIT_PER_MINUTE: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
