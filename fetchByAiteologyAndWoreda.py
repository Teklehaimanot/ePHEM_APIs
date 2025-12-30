import json
import requests

url = "http://localhost:8069/jsonrpc"

# Domain filter by aetiology name and sub-district names
domain = [
    ("aetiology_id.code", "=", "CHOLERA"),
    ("sub_district_ids.name", "in", ["Addis Ketema", "BOLE"])
]

payload = {
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "service": "object",
        "method": "execute_kw",
        "args": [
            "ephem20",
            2,
            "admin",
            "eoc.signal",
            "search_read",
            [domain],  # Domain filter
            {"fields": ["id", "name", "aetiology_id", "active", "sub_district_ids"]}
        ]
    },
    "id": 10,
}

response = requests.post(url, json=payload)
signals = response.json().get("result", [])
print(json.dumps(signals, indent=2))
print (signals.__len__())
