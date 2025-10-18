# import requests

# Notion_Token = ''
# Database_ID = ''

# url = f"https://api.notion.com/v1/databases/{Database_ID}/query"

# headers = {
#     "Authorization": f"Bearer {Notion_Token}",
#     "Notion-Version": "2022-06-28",
#     "Content-Type": "application/json"
# }

# res = requests.post(url, headers=headers)
# data = res.json()

# for page in data["results"]:
#     props = page["properties"]
#     name = props["Name"]["title"][0]["plain_text"] if props["Name"]["title"] else "No Name"
#     date = props["Date"]["date"]["start"] if props["Date"]["date"] else "No Date"
#     print(f"🧾 {name} — 📅 {date}")

import requests

Notion_Token = 'YOUR_NOTOIN_TOKEN'
Database_ID = 'YOUR_NOTION_DB_ID'

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
        else:
            add_to_notion(line)
