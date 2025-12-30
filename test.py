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
            "ephem20",                # Odoo database
            2,                        # User ID (e.g., admin UID)
            "admin",   # Password or API key
            "eoc.signal",       # Odoo model
            "create",                 # Method to call
            [{
                "name": "Cholera in City X",
                "aetiology_id": 83,
                "active": "True"
                # "last_update": "2025-09-10 12:34:00"
            }]
        ]
    },
    "id": 1,
}

response = requests.post(url, json=payload)
print(response.json())
