import os
import json
import base64
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

load_dotenv()

def decrypt_secrets(password: str) -> dict:
    if not os.path.exists("secrets.enc"):
        return {}
    try:
        with open("secrets.enc", "rb") as f_in:
            data = f_in.read()
            salt = data[:16]
            encrypted_data = data[16:]
        
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        f = Fernet(key)
        return json.loads(f.decrypt(encrypted_data).decode())
    except Exception:
        return {}

# Load encrypted secrets if password is provided
ORVION_PWD = os.getenv("ORVION_PWD", "ORVION_SECURE_2026")
secrets_vault = decrypt_secrets(ORVION_PWD)

PROJECT_NAME = "ORVION"
PROJECT_VERSION = "1.0.0"
API_V1_STR = "/api/v1"

# Circle API Configuration
CIRCLE_API_KEY = os.getenv("CIRCLE_API_KEY") or secrets_vault.get("CIRCLE_API_KEY")
CIRCLE_ENTITY_SECRET = os.getenv("ENTITY_SECRET") or secrets_vault.get("ENTITY_SECRET")
ENTITY_SECRET = CIRCLE_ENTITY_SECRET
WALLET_SET_ID = os.getenv("WALLET_SET_ID") or secrets_vault.get("WALLET_SET_ID")

# Arc Network Configuration
ARC_RPC_URL = os.getenv("ARC_RPC_URL", "https://rpc.testnet.arc.network")
PRIVATE_KEY = os.getenv("PRIVATE_KEY") or secrets_vault.get("PRIVATE_KEY")
ESCROW_CONTRACT_ADDRESS = os.getenv("ESCROW_CONTRACT_ADDRESS", "0x0000000000000000000000000000000000000000")

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./orvion.db")

class Settings:
    PROJECT_NAME = PROJECT_NAME
    PROJECT_VERSION = PROJECT_VERSION
    API_V1_STR = API_V1_STR
    CIRCLE_API_KEY = CIRCLE_API_KEY
    CIRCLE_ENTITY_SECRET = CIRCLE_ENTITY_SECRET
    ENTITY_SECRET = ENTITY_SECRET
    WALLET_SET_ID = WALLET_SET_ID
    ARC_RPC_URL = ARC_RPC_URL
    PRIVATE_KEY = PRIVATE_KEY
    ESCROW_CONTRACT_ADDRESS = ESCROW_CONTRACT_ADDRESS
    DATABASE_URL = DATABASE_URL
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-for-dev")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

settings = Settings()
