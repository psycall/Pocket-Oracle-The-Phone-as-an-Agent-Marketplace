import os
import requests
import uuid
import base64
from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

load_dotenv()

API_KEY = os.getenv("CIRCLE_API_KEY")
ENTITY_SECRET = os.getenv("ENTITY_SECRET")
PUBLIC_KEY_PEM = """-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA2Duvi2rJl7sVtyyZrSbr
QZGn8rFKEMo4qIQ6BPjbJ8+rOmYHWJHlbHX/66e2O4D2E8L1kjjiU3SZNAbvkzgM
3IYnsjNEG6VIOAKgYrELX4y4Okzdkg55K6YhJ8hV11yOzzwf60/ZtWu+znXRny8X
YxnzzdChAYXLq6E5Re2JbJ7I1JOY52z3rRuOPnennEx+pZnCPB7M3K814a2FRJa5
Svu8PJdli2ouZ+jphbBTdhvsdX6wUMu4hwPkbfF4dTFpDP7jqXaZBl6cNo+xWvw1
qrRuGzhSCwfK9+vN3rn3K8gQ5XmfmAd46MXhhtPrK48FkChxgXQPqfPetjiTAevN
awNc+UI3oMR1GoRsALoSuyE6bdmGjlEzPURxgzLNiAi8FiRXfvx2rZPS4+C95WBl
ytQdi6IjuDW+wfhMcjD1h0XxgdY+faKZmjJtr6roqgXXC+iNNDntX90Qcwdl1/3k
E+sxXpAmVIALM8D6+qtmNpu7o+Vhq98UE1mm+azalw+kgRXW7+s3H3J8DIDMzJTR
BAptXeUCZxvdkGWYb0xT/IoUMDLF4PGENGJjwEF8093+eLgpOOsFKSmwWzfv4ZNM
8ZApGa0JoHRAu4lIpBWHG67b3bfcK/93GGO97GBZw66ua6EAgFjGDpNPQjY2mZ2G
QBeyxZHi7rUNodCbnYcG8U0CAwEAAQ==
-----END PUBLIC KEY-----"""

def encrypt_entity_secret(entity_secret, public_key_pem):
    public_key = serialization.load_pem_public_key(public_key_pem.encode())
    entity_secret_bytes = bytes.fromhex(entity_secret)
    ciphertext = public_key.encrypt(
        entity_secret_bytes,
        padding.PKCS1v15()
    )
    return base64.b64encode(ciphertext).decode()

def setup():
    ciphertext = encrypt_entity_secret(ENTITY_SECRET, PUBLIC_KEY_PEM)
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {API_KEY}"
    }
    
    # Create Wallet Set
    print("Creating Production Wallet Set...")
    ws_url = "https://api.circle.com/v1/w3s/developer/walletSets"
    ws_payload = {
        "idempotencyKey": str(uuid.uuid4()),
        "name": "ORVION_PROD_SET",
        "entitySecretCiphertext": ciphertext
    }
    ws_res = requests.post(ws_url, json=ws_payload, headers=headers)
    
    if ws_res.status_code == 201:
        ws_id = ws_res.json()['data']['walletSet']['id']
        print(f"✅ Wallet Set Created: {ws_id}")
        
        # Create Wallet
        print("Creating Production Wallet (Polygon)...")
        w_url = "https://api.circle.com/v1/w3s/developer/wallets"
        w_payload = {
            "idempotencyKey": str(uuid.uuid4()),
            "accountType": "SCA",
            "blockchains": ["MATIC"],
            "count": 1,
            "walletSetId": ws_id,
            "entitySecretCiphertext": ciphertext
        }
        w_res = requests.post(w_url, json=w_payload, headers=headers)
        
        if w_res.status_code == 201:
            wallet = w_res.json()['data']['wallets'][0]
            print(f"✅ Wallet Created: {wallet['address']} (ID: {wallet['id']})")
            
            # Update .env
            with open("/home/ubuntu/ORVION/.env", "a") as f:
                f.write(f"\nPROD_WALLET_SET_ID={ws_id}")
                f.write(f"\nPROD_WALLET_ID={wallet['id']}")
                f.write(f"\nPROD_WALLET_ADDRESS={wallet['address']}")
            print("\n🚀 Production Infrastructure Ready!")
        else:
            print(f"❌ Failed to create Wallet: {w_res.text}")
    else:
        print(f"❌ Failed to create Wallet Set: {ws_res.text}")

if __name__ == "__main__":
    setup()
