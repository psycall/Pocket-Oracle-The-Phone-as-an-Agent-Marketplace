
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ORVION - The Agentic Settlement Layer"
    PROJECT_VERSION: str = "2.0.0"

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    REDIS_URL: str = os.getenv("REDIS_URL")
    NEO4J_URI: str = os.getenv("NEO4J_URI")
    NEO4J_USER: str = os.getenv("NEO4J_USER")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD")

    # Arc Network settings
    ARC_RPC_URL: str = os.getenv("ARC_RPC_URL")
    USDC_CONTRACT: str = os.getenv("USDC_CONTRACT")
    ARC_CHAIN_ID: int = int(os.getenv("ARC_CHAIN_ID"))

    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

    # API settings
    API_V1_STR: str = "/api/v1"

    # Circle API settings
    CIRCLE_API_KEY: str = os.getenv("CIRCLE_API_KEY")
    CIRCLE_ENTITY_SECRET: str = os.getenv("CIRCLE_ENTITY_SECRET")
    CIRCLE_WALLET_SET_ID: str = os.getenv("CIRCLE_WALLET_SET_ID")
    CIRCLE_ENV: str = os.getenv("CIRCLE_ENV", "sandbox")
    CIRCLE_BASE_URL: str = os.getenv("CIRCLE_BASE_URL", "https://api-sandbox.circle.com")

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore" # Allow extra fields in .env without error

settings = Settings()
