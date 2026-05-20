import os
import requests
import uuid
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CIRCLE_API_KEY")

def create_wallet_set():
    url = "https://api.circle.com/v1/w3s/walletSets"
    payload = {
        "idempotencyKey": str(uuid.uuid4()),
        "name": "ORVION_PRODUCTION_SET"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {API_KEY}"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        new_id = response.json().get('data', {}).get('walletSet', {}).get('id')
        print(f"✅ Wallet Set Created: {new_id}")
        return new_id
    else:
        print(f"❌ Failed to create Wallet Set: {response.text}")
        return None

if __name__ == "__main__":
    create_wallet_set()
