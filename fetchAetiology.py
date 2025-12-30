import json
import requests

# Configuration
url = "http://localhost:8069/jsonrpc"
db = "ephem20"
uid = 2              # Odoo user ID
password = "admin"
model_name = "aetiology"  # replace with your technical model name

# Optional: filter records
domain = []  # empty = fetch all records
fields = ["id", "name", "code","specific_hazard_id","health_interface_ids","general_hazard_id"]  # list fields you want

# JSON-RPC payload
payload = {
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "service": "object",
        "method": "execute_kw",
        "args": [
            db,
            uid,
            password,
            model_name,
            "search_read",  # combined search and read
            [domain],
            {"fields": fields}
        ]
    },
    "id": 1
}

response = requests.post(url, json=payload)
response.raise_for_status()

records = response.json().get("result", [])
print(json.dumps(records, indent=2))
print(f"Total records: {len(records)}")
