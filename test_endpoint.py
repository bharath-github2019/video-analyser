import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Test Shared Service
url = f"{os.getenv('SHARED_SERVICE_BASE_URL')}/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {os.getenv('SHARED_SERVICE_API_KEY')}",
    "Content-Type": "application/json"
}
payload = {
    "model": os.getenv("SHARED_SERVICE_MODEL"),
    "messages": [{"role": "user", "content": "Say hello"}],
    "max_tokens": 50
}

print("Testing Shared Service...")
r = requests.post(url, headers=headers, json=payload)
print(f"Status: {r.status_code}")
print(f"Response: {r.text[:500]}")
