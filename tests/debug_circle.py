import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("CIRCLE_API_KEY")

def debug():
    # Test different endpoints to see what's available
    endpoints = [
        "https://api.circle.com/v1/configuration/developer/key",
        "https://api.circle.com/v1/w3s/walletSets",
        "https://api.circle.com/v1/w3s/wallets"
    ]
    headers = {"authorization": f"Bearer {API_KEY}"}
    
    for url in endpoints:
        res = requests.get(url, headers=headers)
        print(f"URL: {url} | Status: {res.status_code}")
        if res.status_code == 200:
            print(f"Data: {res.json().get('data', 'No data field')}")

if __name__ == "__main__":
    debug()
