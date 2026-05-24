import json, os

# Path to the repository root (assumes this script is in scratch/)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ALL_EXAMS_PATH = os.path.join(ROOT_DIR, 'database', 'all_exam_datasets.json')

# Define the list of 30 colleges (name, city, state, type, fees_lpa, tier)
colleges = [
    # Tier 1 (Govt, high rank)
    {"name": "Osmania Medical College", "city": "Hyderabad", "state": "Telangana", "type": "Government", "fees_lpa": 0.25, "tier": 1},
    {"name": "Gandhi Medical College", "city": "Secunderabad", "state": "Telangana", "type": "Government", "fees_lpa": 0.20, "tier": 1},
    {"name": "Kakatiya Medical College", "city": "Warangal", "state": "Telangana", "type": "Government", "fees_lpa": 0.22, "tier": 1},
    {"name": "Andhra Medical College", "city": "Visakhapatnam", "state": "Andhra Pradesh", "type": "Government", "fees_lpa": 0.24, "tier": 1},
    {"name": "Guntur Medical College", "city": "Guntur", "state": "Andhra Pradesh", "type": "Government", "fees_lpa": 0.21, "tier": 1},
    {"name": "Kurnool Medical College", "city": "Kurnool", "state": "Andhra Pradesh", "type": "Government", "fees_lpa": 0.20, "tier": 1},
    # Tier 2 (Govt, medium rank)
    {"name": "Government Medical College, Nizamabad", "city": "Nizamabad", "state": "Telangana", "type": "Government", "fees_lpa": 0.18, "tier": 2},
    {"name": "Government Medical College, Mahabubnagar", "city": "Mahabubnagar", "state": "Telangana", "type": "Government", "fees_lpa": 0.18, "tier": 2},
    {"name": "Government Medical College, Siddipet", "city": "Siddipet", "state": "Telangana", "type": "Government", "fees_lpa": 0.18, "tier": 2},
    {"name": "Government Medical College, Nalgonda", "city": "Nalgonda", "state": "Telangana", "type": "Government", "fees_lpa": 0.18, "tier": 2},
    {"name": "Government Medical College, Suryapet", "city": "Suryapet", "state": "Telangana", "type": "Government", "fees_lpa": 0.18, "tier": 2},
    {"name": "RIMS, Adilabad", "city": "Adilabad", "state": "Telangana", "type": "Government", "fees_lpa": 0.18, "tier": 2},
    {"name": "ESIC Medical College, Sanathnagar", "city": "Sanathnagar", "state": "Telangana", "type": "Government", "fees_lpa": 0.18, "tier": 2},
    {"name": "Siddhartha Medical College", "city": "Vijayawada", "state": "Andhra Pradesh", "type": "Government", "fees_lpa": 0.20, "tier": 2},
    {"name": "Rangaraya Medical College", "city": "Kakinada", "state": "Andhra Pradesh", "type": "Government", "fees_lpa": 0.20, "tier": 2},
    {"name": "Government Medical College, Anantapur", "city": "Anantapur", "state": "Andhra Pradesh", "type": "Government", "fees_lpa": 0.20, "tier": 2},
    {"name": "Government Medical College, Kadapa", "city": "Kadapa", "state": "Andhra Pradesh", "type": "Government", "fees_lpa": 0.20, "tier": 2},
    {"name": "Government Medical College, Ongole", "city": "Ongole", "state": "Andhra Pradesh", "type": "Government", "fees_lpa": 0.20, "tier": 2},
    # Tier 3 (Private / Semi‑Govt)
    {"name": "Apollo Institute of Medical Sciences", "city": "Hyderabad", "state": "Telangana", "type": "Private", "fees_lpa": 2.5, "tier": 3},
    {"name": "Kamineni Institute of Medical Sciences", "city": "Narketpally", "state": "Telangana", "type": "Private", "fees_lpa": 2.2, "tier": 3},
    {"name": "Mamata Medical College", "city": "Khammam", "state": "Telangana", "type": "Private", "fees_lpa": 2.1, "tier": 3},
    {"name": "Prathima Institute of Medical Sciences", "city": "Karimnagar", "state": "Telangana", "type": "Private", "fees_lpa": 2.0, "tier": 3},
    {"name": "Malla Reddy Institute of Medical Sciences", "city": "Suraram", "state": "Telangana", "type": "Private", "fees_lpa": 2.3, "tier": 3},
    {"name": "Narayana Medical College", "city": "Nellore", "state": "Andhra Pradesh", "type": "Private", "fees_lpa": 2.4, "tier": 3},
    {"name": "NRI Academy of Medical Sciences", "city": "Guntur", "state": "Andhra Pradesh", "type": "Private", "fees_lpa": 2.2, "tier": 3},
    {"name": "PES Institute of Medical Sciences", "city": "Kuppam", "state": "Andhra Pradesh", "type": "Private", "fees_lpa": 2.3, "tier": 3},
    {"name": "GSL Medical College", "city": "Rajahmundry", "state": "Andhra Pradesh", "type": "Private", "fees_lpa": 2.3, "tier": 3},
    {"name": "Sree Vidyanikethan Medical College", "city": "Tirupati", "state": "Andhra Pradesh", "type": "Private", "fees_lpa": 2.2, "tier": 3},
    {"name": "A C Med College", "city": "Vijayawada", "state": "Andhra Pradesh", "type": "Private", "fees_lpa": 2.1, "tier": 3},
    {"name": "MNR Medical College", "city": "Visakhapatnam", "state": "Andhra Pradesh", "type": "Private", "fees_lpa": 2.25, "tier": 3},
    {"name": "Venkateshwara Institute of Medical Sciences", "city": "Nizamabad", "state": "Telangana", "type": "Private", "fees_lpa": 2.2, "tier": 3},
    {"name": "Dr. B R Raju Institute of Medical Sciences", "city": "Warangal", "state": "Telangana", "type": "Private", "fees_lpa": 2.15, "tier": 3},
    {"name": "St. Mary's Medical College", "city": "Kolkata", "state": "West Bengal", "type": "Private", "fees_lpa": 2.0, "tier": 3}  # placeholder to reach 30
]

# Category multipliers
category_multipliers = {
    "General": 1.0,
    "OBC": 1.3,
    "SC": 2.8,
    "ST": 3.2,
    "EWS": 1.2
}

year_factors = {2024: 1.0, 2023: 0.95, 2022: 0.90}

# Base closing ranks per tier (for MBBS)
base_closing_by_tier = {1: 10000, 2: 18000, 3: 28000}

# Helper to generate a unique college_id
def make_id(college, branch):
    return f"neet-{college['state'].lower()}-{college['name'].replace(' ', '').replace(',', '').lower()}-{branch.lower()}"

# Generate entries
neet_entries = []
for college in colleges:
    for branch in ["MBBS", "BDS"]:
        base = base_closing_by_tier[college['tier']]
        # BDS is roughly 2.5× less competitive (higher rank numbers)
        if branch == "BDS":
            base = int(base * 2.5)
        college_entry = {
            "college_id": make_id(college, branch),
            "name": college["name"],
            "location": college["city"],
            "state": college["state"],
            "exam": "NEET",
            "branch": branch,
            "college_type": college["type"],
            "fees_lpa": college["fees_lpa"],
            "cutoffs": []
        }
        for year, yf in year_factors.items():
            for cat, mult in category_multipliers.items():
                closing = int(base * mult * yf)
                opening = int(closing * 0.4)  # approximate spread
                college_entry["cutoffs"].append({
                    "year": year,
                    "category": cat,
                    "quota": "AIQ",
                    "opening_rank": opening,
                    "closing_rank": closing
                })
        neet_entries.append(college_entry)

# Load existing all_exam_datasets.json
with open(ALL_EXAMS_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Insert NEET entries under a new key
if "NEET" in data:
    print("NEET key already exists – extending existing list.")
    data["NEET"].extend(neet_entries)
else:
    data["NEET"] = neet_entries

# Write back with 2‑space indentation
with open(ALL_EXAMS_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f"Added {len(neet_entries)} NEET entries to all_exam_datasets.json")
