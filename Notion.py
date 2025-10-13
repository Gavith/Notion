# import requests
# from datetime import datetime, timezone

# Notion_Token = 'YOUR_NOTION_TOKEN'
# Database_ID = 'YOUR_DATABASE_ID'

# url = f"https://api.notion.com/v1/databases/{Database_ID}"

# headers = {
#     "Authorization": f"Bearer {Notion_Token}",
#     "Notion-Version": "2022-06-28"
# }

# res = requests.get(url, headers=headers)
# print(res.json())

import requests

Notion_Token = 'YOUR_NOTOIN_TOKE'
Database_ID = 'YOUR_NOTION_ID'

url = f"https://api.notion.com/v1/databases/{Database_ID}/query"

headers = {
    "Authorization": f"Bearer {Notion_Token}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

res = requests.post(url, headers=headers)
data = res.json()

for page in data["results"]:
    props = page["properties"]
    name = props["Name"]["title"][0]["plain_text"] if props["Name"]["title"] else "No Name"
    date = props["Date"]["date"]["start"] if props["Date"]["date"] else "No Date"
    print(f"🧾 {name} — 📅 {date}")
