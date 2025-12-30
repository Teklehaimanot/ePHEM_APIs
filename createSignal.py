import json
import requests
from datetime import date

# ----------------------------
# Configuration
# ----------------------------
url = "http://localhost:8069/jsonrpc"  # Odoo JSON-RPC endpoint
db = "ephem20"                         # Odoo database
username = "admin"                      # Odoo user
password = "admin"                      # User password

# ----------------------------
# Input data
# ----------------------------
signal_name = "New Cholera Signal from DHIS2/IDSR"
aetiology_id = 83 
general_hazard_id=13
specific_hazard_id=92
health_interface_ids=[1,3]                # ID of the aetiology (must exist)
sub_district_name = "BOLE"   # Name of the sub-district
report_date = str(date.today())

# ----------------------------
#  Create signal
# ----------------------------
payload_create = {
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "service": "object",
        "method": "execute_kw",
        "args": [
            db,
            2,  # UID
            password,
            "eoc.signal",
            "create",
            [{
                "name": signal_name,
                "aetiology_id": aetiology_id,             # many2one
                "general_hazard_id": general_hazard_id,   # many2one
                "specific_hazard_id": specific_hazard_id, # many2one
                "health_interface_ids": [(6, 0, health_interface_ids)],  # many
                "report_date": report_date,
                "active": True,

                'sub_district_ids': [(6, 0, [3189])],
                'district_ids': [(6, 0, [14248])],
                'state_ids': [(6, 0, [11618])],
                'country_ids': [(6, 0, [69])],
                'title_prefix': 'DHIS2/IDSR, Week-44 report',
                'people_affected': '1',
                'incident_date': date.today().isoformat()
            }]
        ]
    },
    "id": 2
}

response_create = requests.post(url, json=payload_create)
response_create.raise_for_status()
data_create = response_create.json()

if "error" in data_create:
    print("Error creating signal:", data_create["error"])
else:
    new_signal_id = data_create.get("result")
    print(f"Signal created successfully with ID: {new_signal_id}")
