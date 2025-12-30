
from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Odoo connection config
URL = "http://localhost:8069/jsonrpc"
DB = "ephem20"
UID = 2
PASSWORD = "admin"
MODEL_NAME = "aetiology"

FIELDS = [
    "id",
    "name",
    "code",
    "specific_hazard_id",
    "general_hazard_id",
    "health_interface_ids",
]


@app.route("/api/aetiologies", methods=["GET"])
def get_aetiologies():
    try:
        # JSON-RPC payload for Odoo
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    DB,
                    UID,
                    PASSWORD,
                    MODEL_NAME,
                    "search_read",
                    [[]],  # Empty domain = all records
                    {"fields": FIELDS},
                ],
            },
            "id": 1,
        }

        response = requests.post(URL, json=payload)
        response.raise_for_status()
        records = response.json().get("result", [])

        # Flatten many2one fields
        formatted_records = []
        for rec in records:
            formatted_record = {
                "id": rec.get("id"),
                "name": rec.get("name"),
                "code": rec.get("code"),
                "specific_hazard_id": rec["specific_hazard_id"][0] if rec.get("specific_hazard_id") else None,
                "specific_hazard": rec["specific_hazard_id"][1] if rec.get("specific_hazard_id") else None,
                "general_hazard_id": rec["general_hazard_id"][0] if rec.get("general_hazard_id") else None,
                "general_hazard": rec["general_hazard_id"][1] if rec.get("general_hazard_id") else None,
                "health_interface_ids": rec.get("health_interface_ids", []),
            }
            formatted_records.append(formatted_record)

        return jsonify({"status": "success", "total": len(formatted_records), "data": formatted_records})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
