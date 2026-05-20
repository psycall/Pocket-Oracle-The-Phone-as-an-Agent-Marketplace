import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CIRCLE_API_KEY")
WALLET_SET_ID = os.getenv("WALLET_SET_ID")

def test_connection():
    url = "https://api.circle.com/v1/w3s/walletSets"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {API_KEY}"
    }
    
    print(f"Testing connection to Circle API...")
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("✅ Connection Successful!")
            wallet_sets = response.json().get('data', {}).get('walletSets', [])
            found = any(ws.get('id') == WALLET_SET_ID for ws in wallet_sets)
            if found:
                print(f"✅ Wallet Set ID {WALLET_SET_ID} found and active.")
            else:
                print(f"⚠️ Connection OK, but Wallet Set ID {WALLET_SET_ID} not found in this account.")
        else:
            print(f"❌ Connection Failed. Status Code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_connection()
