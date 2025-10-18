import requests
import re

Notion_Token = 'YOUR_NOTION_TOKEN'
Database_ID = 'YOUR_NOTION_ID'

url = "https://api.notion.com/v1/pages"

headers = {
    "Authorization": f"Bearer {Notion_Token}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def add_to_notion(title, date=None):
    payload = {
        "parent": {"database_id": Database_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": title}}]}
        }
    }
    if date:
        payload["properties"]["Date"] = {"date": {"start": date}}

    res = requests.post(url, headers=headers, json=payload)
    if res.status_code == 200:
        print(f"✅ Added: {title}")
    else:
        print(f"❌ Failed to add {title} — {res.status_code}")
        print(res.text)

# -----------------------------------------------------------------------------------------------------

with open('Recording.txt', 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        if not line or line.startswith('Topic'):
            continue
        
        # 🧼 Remove numbers like 1. 2. 10. etc.
        line = re.sub(r'^\d+\.\s*', '', line)

        add_to_notion(line)
