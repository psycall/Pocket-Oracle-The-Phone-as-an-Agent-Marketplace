import os
import json
import base64
import argparse
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def get_key_from_password(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_secrets(password: str, secrets: dict):
    salt = os.urandom(16)
    key = get_key_from_password(password, salt)
    f = Fernet(key)
    
    encrypted_data = f.encrypt(json.dumps(secrets).encode())
    
    with open("secrets.enc", "wb") as f_out:
        f_out.write(salt + encrypted_data)
    
    print("✅ Secrets encrypted and saved to secrets.enc")

def decrypt_secrets(password: str) -> dict:
    if not os.path.exists("secrets.enc"):
        print("❌ secrets.enc not found.")
        return None
        
    with open("secrets.enc", "rb") as f_in:
        data = f_in.read()
        salt = data[:16]
        encrypted_data = data[16:]
        
    key = get_key_from_password(password, salt)
    f = Fernet(key)
    
    try:
        decrypted_data = f.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode())
    except Exception:
        print("❌ Invalid password or corrupted data.")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ORVION Secure Key Manager")
    parser.add_argument("--init", action="store_true", help="Initialize encrypted vault")
    parser.add_argument("--decrypt", action="store_true", help="Test decryption")
    
    args = parser.parse_args()
    
    if args.init:
        # Secrets should be provided via environment variables or interactive input
        secrets = {
            "CIRCLE_API_KEY": os.getenv("CIRCLE_API_KEY"),
            "ENTITY_SECRET": os.getenv("ENTITY_SECRET"),
            "WALLET_SET_ID": os.getenv("WALLET_SET_ID"),
            "PRIVATE_KEY": os.getenv("PRIVATE_KEY"),
            "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN")
        }
        
        # Check if all secrets are provided
        if not all(secrets.values()):
            print("❌ Missing environment variables. Please set CIRCLE_API_KEY, ENTITY_SECRET, WALLET_SET_ID, PRIVATE_KEY, and GITHUB_TOKEN.")
            exit(1)
        
        password = input("Enter password to protect your keys: ") if not os.getenv("ORVION_PWD") else os.getenv("ORVION_PWD")
        if not password:
            password = "ORVION_SECURE_2026" # Default for automation if not provided
            
        encrypt_secrets(password, secrets)
        
        if os.path.exists(".env"):
            os.remove(".env")
            print("🗑️ Original .env removed for security.")
            
    elif args.decrypt:
        password = input("Enter password: ")
        secrets = decrypt_secrets(password)
        if secrets:
            print("✅ Decryption successful.")
            # print(secrets) # Don't print in production
