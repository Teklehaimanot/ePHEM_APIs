#!/usr/bin/env python3
import xmlrpc.client
import json
import pandas as pd

# Replace with your ePHEM server URL, e.g., 'http://localhost:8069'
url = 'https://testc.pheoc.com'
db = 'testc'
username = 'API_ARAFAT'
password = '4ad2a8b33e9dbe7b34abd0927281d74a26fe56cb'

# --- Connect to ePHEM ---
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
if not uid:
    raise Exception("Authentication failed. Check your credentials.")

models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# ============================================================
# Part 1: Fetch and export eoc.signal records
# ============================================================
# --- Define important fields for eoc.signal ---
fields_to_fetch = [
    "signal_seq",                # Signal ID
    "name",                      # Signal Title
    "title_prefix",              # Mini Title
    "description",               # Narrative Description
    "incident_date",             # Incident Date
    "report_date",               # Detection Date
    "create_date",               # Creation Date
    "active",                    # Active flag
    "user_id",                   # Signal Lead
    "signal_type",               # Signal Type
    "signal_stage_state_id",     # Signal Stage (ID)
    "signal_stage_state_name",   # Signal Stage Name
    "verification",              # Verification status
    "outcome",                   # Final Outcome
    "people_affected",           # People affected
    "fatalities",                # Fatalities
    "address",                   # Address
    "latitude",                  # Latitude coordinate
    "longitude",                 # Longitude coordinate
    "confidentiality",
    "signal_type",
    "verification",
    "signal_state_health_interface",
    "was_event",
    "was_under_verification",
    "was_closed",
    "was_closed_date",
    "was_discarded_date",
    "state_ids_names_string",
    "source_country_id",
    "aetiology_id_Related",
    "general_hazard_id",
    "specific_hazard_id",
    "health_facilities_affected",
    "health_care_workers_affected",
    "houses_affected",
    "animals_affected",
    "is_triaged",
    "is_discarded",
    "is_verification_initiated",
    "is_verified",
    "verified_date",
    "verification_source_id",
    "is_risk_assessed",
    "is_incident",
    "ebase_outcome_justification_id",
    "is_event_closed",
    "date_closed",
]

# --- Fetch eoc.signal records ---
signals = models.execute_kw(
    db, uid, password,
    'eoc.signal', 'search_read',
    [[]],  # Empty domain: fetch all records
    {'fields': fields_to_fetch}
)

# --- Preprocess records: Replace False values with the string "null" ---
for record in signals:
    for field in list(record.keys()):
        if record[field] is False:
            record[field] = "null"

# --- Save signals to JSON ---
json_filename_signals = 'signals_identified.json'
with open(json_filename_signals, 'w', encoding='utf-8') as json_file:
    json.dump(signals, json_file, indent=4, ensure_ascii=False)
print(f"Saved signals JSON data to '{json_filename_signals}'.")

# --- Save signals to Excel ---
excel_filename_signals = 'signals_identified.xlsx'
if signals:
    df_signals = pd.DataFrame(signals)
    df_signals.to_excel(excel_filename_signals, index=False)
    print(f"Saved signals Excel data to '{excel_filename_signals}'.")
else:
    print("No signal records found to save.")

# ============================================================
# Part 2: Fetch and export eoc.signal.sources records
# ============================================================
# --- Define fields to fetch for eoc.signal.sources ---
source_fields_to_fetch = [
    "id",                  # Primary key
    "created_by",
    "signal_id",
    "source_type",         # Many2one field (will be returned as [id, display_name])
    "name",
    "source_phone",
    "source_address",
    "publication_date",
    "attachment_ids",
]

# --- Fetch eoc.signal.sources records ---
sources = models.execute_kw(
    db, uid, password,
    "eoc.signal.sources", "search_read",
    [[]],  # Fetch all records
    {"fields": source_fields_to_fetch}
)

# --- Process each source record to extract the source_type name ---
for record in sources:
    if record.get("source_type") and isinstance(record["source_type"], list):
        # source_type is a list like [id, "Source Type Name"]
        record["source_type_name"] = record["source_type"][1]
    else:
        record["source_type_name"] = None

# --- Save sources to JSON ---
json_filename_sources = 'sources_identified.json'
with open(json_filename_sources, 'w', encoding='utf-8') as json_file:
    json.dump(sources, json_file, indent=4, ensure_ascii=False)
print(f"Saved sources JSON data to '{json_filename_sources}'.")

# --- Save sources to Excel ---
excel_filename_sources = 'sources_identified.xlsx'
if sources:
    df_sources = pd.DataFrame(sources)
    df_sources.to_excel(excel_filename_sources, index=False)
    print(f"Saved sources Excel data to '{excel_filename_sources}'.")
else:
    print("No source records found to save.")