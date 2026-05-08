
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ORVION - The Agentic Settlement Layer"
    PROJECT_VERSION: str = "2.0.0"

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://orvion:orvion@localhost:5432/orvion")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER: str = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "orvion_secure_password")

    # Arc Network settings
    ARC_RPC_URL: str = os.getenv("ARC_RPC_URL", "https://testnet-rpc.arc.network")
    USDC_CONTRACT: str = os.getenv("USDC_CONTRACT", "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913")
    ARC_CHAIN_ID: int = int(os.getenv("ARC_CHAIN_ID", "2602"))

    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # API settings
    API_V1_STR: str = "/api/v1"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
