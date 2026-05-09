
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
    USDC_CONTRACT: str = os.getenv("USDC_CONTRACT", os.getenv("USDC_ADDRESS", "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"))
    CIRBTC_CONTRACT: str = os.getenv("CIRBTC_CONTRACT", "0x5412177bEEB84dD86E0f0e6cc54651D5bbB4264D") # Endereço fictício para cirBTC
    ARC_CHAIN_ID: int = int(os.getenv("ARC_CHAIN_ID", "5042002"))

    # Pharos Network settings (CCTP v2)
    PHAROS_RPC_URL: str = os.getenv("PHAROS_RPC_URL", "https://rpc.testnet.pharos.network")
    PHAROS_CHAIN_ID: int = int(os.getenv("PHAROS_CHAIN_ID", "808080")) # Exemplo de Chain ID para Pharos
    PHAROS_USDC_CONTRACT: str = os.getenv("PHAROS_USDC_CONTRACT", "")

    # Smart Contract settings
    SETTLEMENT_CONTRACT_ADDRESS: str = os.getenv(
        "SETTLEMENT_CONTRACT_ADDRESS",
        "0x34B7d77bEEB84dD86E0f0e6cc54651D5bbB4264D"
    )
    PRIVATE_KEY: str = os.getenv("PRIVATE_KEY", "")

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
    
    # Circle Forwarding Service & Nanopayments
    CIRCLE_FORWARDING_SERVICE_URL: str = os.getenv("CIRCLE_FORWARDING_SERVICE_URL", "https://api-sandbox.circle.com/v1/forwarding")
    CIRCLE_GATEWAY_URL: str = os.getenv("CIRCLE_GATEWAY_URL", "https://api-sandbox.circle.com/v1/gateway")

    # Multichain Registry (CCTP Domains & USDC Addresses)
    # Mapping: Domain ID -> {name, chain_id, usdc_address}
    MULTICHAIN_REGISTRY: dict = {
        0: {"name": "Ethereum", "chain_id": 1, "usdc": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eb48"},
        1: {"name": "Avalanche", "chain_id": 43114, "usdc": "0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E"},
        2: {"name": "Optimism", "chain_id": 10, "usdc": "0x0b2C639c533813f4Aa9D7837CAf62653d097ff85"},
        3: {"name": "Arbitrum", "chain_id": 42161, "usdc": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831"},
        5: {"name": "Solana", "chain_id": None, "usdc": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"},
        6: {"name": "Base", "chain_id": 8453, "usdc": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"},
        7: {"name": "Polygon", "chain_id": 137, "usdc": "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359"},
        10: {"name": "Unichain", "chain_id": 130, "usdc": "0x..."},
        13: {"name": "Sonic", "chain_id": 146, "usdc": "0x..."},
        16: {"name": "Sei", "chain_id": 1329, "usdc": "0x..."},
        26: {"name": "Arc", "chain_id": 5042002, "usdc": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"},
        31: {"name": "Pharos", "chain_id": 808080, "usdc": "0x..."},
    }

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore" # Allow extra fields in .env without error

settings = Settings()
