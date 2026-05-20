import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("CIRCLE_API_KEY")

def get_key():
    url = "https://api.circle.com/v1/w3s/config/entity/publicKey"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {API_KEY}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(response.json()['data']['publicKey'])
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    get_key()
