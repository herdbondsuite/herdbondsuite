import os
import requests
import uuid
from datetime import datetime

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_API_KEY = os.environ.get("SUPABASE_API_KEY")
TABLE_NAME = "vendors"

headers = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}

vendor = {
    "id": str(uuid.uuid4()),
    "name": "The Boho Bride Co.",
    "location": "Vero Beach, FL",
    "website": "https://bohobrideco.com",
    "price_range": "$$",
    "style_tags": ["boho", "natural", "earthy"],
    "description": "Boho-style wedding photography and coordination for free-spirited couples.",
    "ai_summary": "Chill, affordable boho-style wedding vendor",
    "source": "manual-entry",
    "created_at": datetime.utcnow().isoformat(),
    "updated_at": datetime.utcnow().isoformat()
}

response = requests.post(
    f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}",
    headers=headers,
    json=[vendor]
)

print("Status:", response.status_code)
print("Response:", response.json())
