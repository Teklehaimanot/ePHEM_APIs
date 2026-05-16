import json
import requests
from itertools import groupby

url = "https://ethiopia.pheoc.com/jsonrpc"

payload = {
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "service": "object",
        "method": "execute_kw",
        "args": [
            "ethiopia",            # Odoo database
            269,                    # User ID (e.g., admin UID)
            "admin",           # Password
            "eoc.signal",          # Odoo model
            "search_read",         # Method
            [                      # Domain filter (empty = all records)
                []
            ],
            {                      # Fields to return (empty = all fields)
                "fields": ["id", "title_prefix", "aetiology_id", "active", "signal_state_health_interface"]
            }
        ]
    },
}

response = requests.post(url, json=payload)

def get_aetiology_id(item):
    aetiology_id = item.get('aetiology_id')
    if isinstance(aetiology_id, list):
        # If it's a list, return the second element (the name of the disease)
        return str(aetiology_id[1]) if len(aetiology_id) > 1 else "Not Set"
    if aetiology_id is False:
        return "Not Set"  # Treat False as "Not Set"
    return str(aetiology_id)  # Ensure it's treated as a string

if response.status_code == 200:
    data = response.json()
    signals = data.get("result", [])
    print(json.dumps(signals, indent=2))  # This prints the full raw response

    if signals:
        print(f"\nTotal records: {len(signals)}")
        
        signals.sort(key=get_aetiology_id)  # Sort by aetiology_id, treating False as "Not Set"
        group_data = groupby(signals, key=get_aetiology_id)
        
        table_data = []
        signal_states = ["info", "relevant", "monitoring", "discarded", "event","closed"]  # Define the signal states to count
        
        for aetiology_id, group in group_data:
            signals = list(group)
            counts = {state: 0 for state in signal_states}

            # Count the occurrences of each state
            for item in signals:
                state = item['signal_state_health_interface'].lower()
                if state in counts:
                    counts[state] += 1
            
            # Collect the row data
            total_count = len(signals)
            row_data = {
                'aetiology': aetiology_id,
                'total': total_count,
                'row_information': counts["info"],
                'triaged': counts["relevant"],
                'incident': counts["event"],
                'discarded': counts["discarded"],
                'monitored': counts["monitoring"],
                'closed': counts["closed"]
            }
            table_data.append(row_data)

        # Now print the table header
        print(f"\n{'Aetiology':<50}{'Total':<8}{'Row Information':<18}{'Triaged':<10}{'Incident':<10}{'Discarded':<12}{'Monitored':<10}{'Closed':<10}")
        print("-" * 100)

        # Print the table rows
        for row in table_data:
            print(f"{str(row['aetiology']):<50}{str(row['total']):<8}{str(row['row_information']):<18}{str(row['triaged']):<10}{str(row['incident']):<10}{str(row['discarded']):<12}{str(row['monitored']):<10}{str(row['closed']):<10}")
else:
    print(f"Error: Received status code {response.status_code}")