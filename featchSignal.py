import json
import requests

url = "http://localhost:8069/jsonrpc"

payload = {
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "service": "object",
        "method": "execute_kw",
        "args": [
            "ephem20",             # Odoo database
            2,                     # User ID (e.g., admin UID)
            "admin",               # Password
            "eoc.signal",          # Odoo model
            "search_read",         # Method
            [                      # Domain filter (empty = all records)
                []
            ],
            {                      # Fields to return (empty = all fields)
                "fields": ["id", "name", "aetiology_id", "active", "sub_district_ids", "dhis2_tei_id"]
            }
        ]
    },
    "id": 2,
}

response = requests.post(url, json=payload)
print(json.dumps(response.json(), indent=2))
