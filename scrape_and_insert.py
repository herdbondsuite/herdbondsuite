import os
import requests
import uuid
from datetime import datetime
from bs4 import BeautifulSoup

# Supabase credentials from GitHub secrets
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_API_KEY = os.environ.get("SUPABASE_API_KEY")
TABLE_NAME = "vendors"

headers = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def fetch_weddingwire_vendors():
    url = "https://www.weddingwire.com/c/florida/wedding-planners/11-sca.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    vendors = []
    listings = soup.select(".vendor-row")[:10]  # Grab 10 vendors

    for vendor in listings:
        name_tag = vendor.select_one(".vendor-name")
        location_tag = vendor.select_one(".locality")
        desc_tag = vendor.select_one(".review-snippet")

        if name_tag:
            vendor_data = {
                "id": str(uuid.uuid4()),
                "name": name_tag.get_text(strip=True),
                "location": location_tag.get_text(strip=True) if location_tag else "Florida",
                "website": "https://www.weddingwire.com" + name_tag.get("href", ""),
                "price_range": "$$",  # Placeholder — we'll improve this later
                "description": desc_tag.get_text(strip=True) if desc_tag else "No description available.",
                "ai_summary": "Wedding vendor from WeddingWire (auto-scraped)",
                "source": "weddingwire.com",
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            vendors.append(vendor_data)

    return vendors

def upload_to_supabase(vendors):
    if not vendors:
        print("No vendors found.")
        return

    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}",
        headers=headers,
        json=vendors
    )
    print("Status:", response.status_code)
    print("Response:", response.json())

if __name__ == "__main__":
    vendor_data = fetch_weddingwire_vendors()
    print("Scraped", len(vendor_data), "vendors.")
    upload_to_supabase(vendor_data)
