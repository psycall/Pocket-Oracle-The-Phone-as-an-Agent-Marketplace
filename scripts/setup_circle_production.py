import os
import requests
import uuid
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CIRCLE_API_KEY")
ENTITY_SECRET = os.getenv("ENTITY_SECRET")

def setup():
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {API_KEY}"
    }
    
    # 1. Create Wallet Set
    print("Creating Production Wallet Set...")
    ws_url = "https://api.circle.com/v1/w3s/developer/walletSets"
    ws_payload = {
        "idempotencyKey": str(uuid.uuid4()),
        "name": "ORVION_PROD_SET"
    }
    ws_res = requests.post(ws_url, json=ws_payload, headers=headers)
    
    if ws_res.status_code != 201:
        print(f"❌ Failed to create Wallet Set: {ws_res.text}")
        return
    
    ws_id = ws_res.json()['data']['walletSet']['id']
    print(f"✅ Wallet Set Created: {ws_id}")
    
    # 2. Create Wallet
    print("Creating Production Wallet (Polygon)...")
    w_url = "https://api.circle.com/v1/w3s/developer/wallets"
    w_payload = {
        "idempotencyKey": str(uuid.uuid4()),
        "accountType": "SCA",
        "blockchains": ["MATIC"],
        "count": 1,
        "walletSetId": ws_id
    }
    w_res = requests.post(w_url, json=w_payload, headers=headers)
    
    if w_res.status_code != 201:
        print(f"❌ Failed to create Wallet: {w_res.text}")
        return
    
    wallet = w_res.json()['data']['wallets'][0]
    print(f"✅ Wallet Created: {wallet['address']} (ID: {wallet['id']})")
    
    # Update .env
    with open("/home/ubuntu/ORVION/.env", "a") as f:
        f.write(f"\nPROD_WALLET_SET_ID={ws_id}")
        f.write(f"\nPROD_WALLET_ID={wallet['id']}")
        f.write(f"\nPROD_WALLET_ADDRESS={wallet['address']}")
    
    print("\n🚀 Production Infrastructure Ready!")

if __name__ == "__main__":
    setup()
