from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Odoo connection config
URL = "http://localhost:8069/jsonrpc"
DB = "ephem20"
UID = 2
PASSWORD = "admin"
MODEL_NAME = "res.country.state.district.sub"  # Correct subdistrict model

FIELDS = [
    "id",
    "name",
    "code",
    "district_id",  # zone
    "state_id",     # region
    "country_id",   # country
]

@app.route("/api/subdistricts", methods=["GET"])
def get_subdistricts():
    try:
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
                    [[]],  # fetch all records
                    {"fields": FIELDS},
                ],
            },
            "id": 1,
        }

        response = requests.post(URL, json=payload)
        response.raise_for_status()
        records = response.json().get("result", [])

        formatted_records = []
        for rec in records:
            formatted_record = {
                "id": rec.get("id"),
                "name": rec.get("name"),
                "code": rec.get("code"),
                "zone_id": rec["district_id"][0] if rec.get("district_id") else None,
                "zone_name": rec["district_id"][1] if rec.get("district_id") else None,
                "region_id": rec["state_id"][0] if rec.get("state_id") else None,
                "region_name": rec["state_id"][1] if rec.get("state_id") else None,
                "country_id": rec["country_id"][0] if rec.get("country_id") else None,
                "country_name": rec["country_id"][1] if rec.get("country_id") else None,
            }
            formatted_records.append(formatted_record)

        return jsonify({"status": "success", "total": len(formatted_records), "data": formatted_records})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
