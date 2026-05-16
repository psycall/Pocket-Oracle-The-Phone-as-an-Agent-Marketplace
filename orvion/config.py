import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME = "ORVION"
PROJECT_VERSION = "1.0.0"
API_V1_STR = "/api/v1"

# Circle API Configuration
CIRCLE_API_KEY = os.getenv("CIRCLE_API_KEY")
CIRCLE_ENTITY_SECRET = os.getenv("ENTITY_SECRET")
WALLET_SET_ID = os.getenv("WALLET_SET_ID")

# Arc Network Configuration
ARC_RPC_URL = os.getenv("ARC_RPC_URL", "https://rpc.testnet.arc.network")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
ESCROW_CONTRACT_ADDRESS = os.getenv("ESCROW_CONTRACT_ADDRESS", "0x0000000000000000000000000000000000000000")

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./orvion.db")

class Settings:
    PROJECT_NAME = PROJECT_NAME
    PROJECT_VERSION = PROJECT_VERSION
    API_V1_STR = API_V1_STR
    CIRCLE_API_KEY = CIRCLE_API_KEY
    CIRCLE_ENTITY_SECRET = CIRCLE_ENTITY_SECRET
    WALLET_SET_ID = WALLET_SET_ID
    ARC_RPC_URL = ARC_RPC_URL
    PRIVATE_KEY = PRIVATE_KEY
    ESCROW_CONTRACT_ADDRESS = ESCROW_CONTRACT_ADDRESS
    DATABASE_URL = DATABASE_URL
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-for-dev")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

settings = Settings()
