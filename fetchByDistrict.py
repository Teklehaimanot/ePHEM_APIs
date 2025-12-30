import json
import requests

url = "http://localhost:8069/jsonrpc"

# Step 1: Fetch signals
payload_signals = {
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
            [[]],   # All signals
            {"fields": ["id", "name", "aetiology_id", "active", "sub_district_ids", "dhis2_tei_id"]}
        ]
    },
    "id": 2,
}

signals = requests.post(url, json=payload_signals).json().get("result", [])

# Step 2: Collect all sub_district IDs
all_sub_ids = set()
for sig in signals:
    all_sub_ids.update(sig.get("sub_district_ids", []))

# Step 3: Fetch sub-district names from res.country.state.district.sub
subdistricts = {}
if all_sub_ids:
    payload_subdistricts = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": "object",
            "method": "execute_kw",
            "args": [
                "ephem20",
                2,
                "admin",
                "res.country.state.district.sub",  # Correct model name
                "search_read",
                [[("id", "in", list(all_sub_ids))]],
                {"fields": ["id", "name"]}
            ]
        },
        "id": 3,
    }
    subdistricts_result = requests.post(url, json=payload_subdistricts).json().get("result", [])
    subdistricts = {sd["id"]: sd["name"] for sd in subdistricts_result}

# Step 4: Merge names into signals
for sig in signals:
    sig["sub_district_names"] = [subdistricts.get(i, f"ID {i}") for i in sig.get("sub_district_ids", [])]

print(json.dumps(signals, indent=2))
