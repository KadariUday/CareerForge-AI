import json
import os
import random

def generate_eamcet_colleges():
    # Base path
    db_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(db_dir, "all_exam_datasets.json")
    
    if not os.path.exists(dataset_path):
        print(f"Error: {dataset_path} not found.")
        return

    # Load existing datasets
    with open(dataset_path, "r", encoding="utf-8") as f:
        all_data = json.load(f)
    
    # We will preserve SVEC Tirupati and Andhra University, but filter out
    # JNTU Hyderabad, Osmania University, and CBIT Hyderabad because we are adding
    # their fully descriptive names instead.
    existing_eamcet = all_data.get("EAMCET", [])
    sved_andhra = []
    for college in existing_eamcet:
        if college.get("name") not in ["JNTU Hyderabad", "Osmania University", "CBIT Hyderabad"]:
            sved_andhra.append(college)
            
    print(f"Preserved {len(sved_andhra)} existing EAMCET entries (e.g. SVEC, Andhra University).")

    # Define the 30 new colleges
    colleges_def = [
        # Tier 1 (CSE closing ~500 - 2500)
        {"id": "jntuh", "name": "JNTUH College of Engineering, Hyderabad", "location": "Hyderabad", "type": "Government", "fees": 0.35, "est": 1965, "nirf": 80, "website": "https://jntuhceh.ac.in", "placement": 8.5, "tier": 1},
        {"id": "ouce", "name": "Osmania University College of Engineering (OUCE), Hyderabad", "location": "Hyderabad", "type": "Government", "fees": 0.35, "est": 1917, "nirf": 88, "website": "https://uceou.edu", "placement": 9.2, "tier": 1},
        {"id": "cbit", "name": "Chaitanya Bharathi Institute of Technology (CBIT), Hyderabad", "location": "Hyderabad", "type": "Private", "fees": 1.4, "est": 1979, "nirf": 120, "website": "https://cbit.ac.in", "placement": 9.0, "tier": 1},
        {"id": "vnrvjiet", "name": "VNR Vignana Jyothi Institute of Engineering and Technology (VNR VJIET), Hyderabad", "location": "Hyderabad", "type": "Private", "fees": 1.35, "est": 1995, "nirf": 113, "website": "https://vnrvjiet.ac.in", "placement": 8.0, "tier": 1},
        {"id": "vce", "name": "Vasavi College of Engineering (VCE), Hyderabad", "location": "Hyderabad", "type": "Private", "fees": 1.3, "est": 1981, "nirf": 150, "website": "https://vce.ac.in", "placement": 8.5, "tier": 1},
        {"id": "kmit", "name": "Keshav Memorial Institute of Technology (KMIT), Hyderabad", "location": "Hyderabad", "type": "Private", "fees": 1.15, "est": 2007, "nirf": None, "website": "https://kmit.in", "placement": 9.7, "tier": 1},
        
        # Tier 2 (CSE closing ~2500 - 7000)
        {"id": "griet", "name": "Gokaraju Rangaraju Institute of Engineering and Technology (GRIET), Hyderabad", "location": "Hyderabad", "type": "Private", "fees": 1.3, "est": 1997, "nirf": 165, "website": "https://griet.ac.in", "placement": 7.5, "tier": 2},
        {"id": "cvr", "name": "CVR College of Engineering, Mangalpally", "location": "Mangalpally", "type": "Private", "fees": 1.5, "est": 2001, "nirf": 170, "website": "https://cvr.ac.in", "placement": 8.0, "tier": 2},
        {"id": "mgit", "name": "Mahatma Gandhi Institute of Technology (MGIT), Hyderabad", "location": "Hyderabad", "type": "Private", "fees": 1.25, "est": 1997, "nirf": None, "website": "https://mgit.ac.in", "placement": 6.8, "tier": 2},
        {"id": "bvrit", "name": "B V Raju Institute of Technology (BVRIT), Narsapur", "location": "Narsapur", "type": "Private", "fees": 1.25, "est": 1997, "nirf": 180, "website": "https://bvrit.ac.in", "placement": 6.5, "tier": 2},
        {"id": "snist", "name": "Sreenidhi Institute of Science and Technology (SNIST), Ghatkesar", "location": "Ghatkesar", "type": "Private", "fees": 1.3, "est": 1997, "nirf": None, "website": "https://sreenidhi.edu.in", "placement": 7.2, "tier": 2},
        {"id": "mvsr", "name": "Maturi Venkata Subba Rao Engineering College (MVSR), Hyderabad", "location": "Hyderabad", "type": "Private", "fees": 1.25, "est": 1981, "nirf": None, "website": "https://mvsrec.edu.in", "placement": 6.2, "tier": 2},
        {"id": "vardhaman", "name": "Vardhaman College of Engineering, Hyderabad", "location": "Hyderabad", "type": "Private", "fees": 1.25, "est": 1999, "nirf": 190, "website": "https://vardhaman.org", "placement": 6.5, "tier": 2},
        {"id": "gnits", "name": "G. Narayanamma Institute of Technology and Science (GNITS - Women), Hyderabad", "location": "Hyderabad", "type": "Private", "fees": 1.22, "est": 1997, "nirf": 195, "website": "https://gnits.ac.in", "placement": 7.5, "tier": 2},
        {"id": "jntuhs", "name": "JNTUH College of Engineering, Sultanpur", "location": "Sultanpur", "type": "Government", "fees": 0.5, "est": 2012, "nirf": None, "website": "https://jntuhces.ac.in", "placement": 5.5, "tier": 2},
        {"id": "kitsw", "name": "Kakatiya Institute of Technology and Science (KITSW), Warangal", "location": "Warangal", "type": "Private", "fees": 1.25, "est": 1980, "nirf": None, "website": "https://kitsw.ac.in", "placement": 6.0, "tier": 2},
        {"id": "bvrith", "name": "BVRIT Hyderabad College of Engineering for Women, Hyderabad", "location": "Hyderabad", "type": "Private", "fees": 1.2, "est": 2012, "nirf": None, "website": "https://bvrithyderabad.edu.in", "placement": 7.0, "tier": 2},

        # Tier 3 (CSE closing ~7000 - 15000)
        {"id": "iare", "name": "Institute of Aeronautical Engineering (IARE), Dundigal", "location": "Dundigal", "type": "Private", "fees": 1.1, "est": 2000, "nirf": None, "website": "https://iare.ac.in", "placement": 5.8, "tier": 3},
        {"id": "anurag", "name": "Anurag University, Hyderabad", "location": "Hyderabad", "type": "Private", "fees": 1.35, "est": 2002, "nirf": None, "website": "https://anurag.edu.in", "placement": 6.2, "tier": 3},
        {"id": "cmrcet", "name": "CMR College of Engineering & Technology (CMRCET), Hyderabad", "location": "Hyderabad", "type": "Private", "fees": 1.15, "est": 2002, "nirf": None, "website": "https://cmrcet.ac.in", "placement": 5.5, "tier": 3},
        {"id": "gcet", "name": "Geethanjali College of Engineering and Technology (GCET), Hyderabad", "location": "Hyderabad", "type": "Private", "fees": 1.1, "est": 2005, "nirf": None, "website": "https://geethanjaliinstitutions.com", "placement": 5.2, "tier": 3},
        {"id": "mecs", "name": "Matrusri Engineering College (MECS), Hyderabad", "location": "Hyderabad", "type": "Private", "fees": 1.15, "est": 2011, "nirf": None, "website": "https://matrusri.edu.in", "placement": 6.0, "tier": 3},
        {"id": "kuce", "name": "Kakatiya University College of Engineering and Technology (KUCE), Warangal", "location": "Warangal", "type": "Government", "fees": 0.35, "est": 2009, "nirf": None, "website": "https://kuce.ac.in", "placement": 5.0, "tier": 3},

        # Tier 4 (CSE closing ~12000 - 26000)
        {"id": "vjit", "name": "Vidya Jyothi Institute of Technology (VJIT), Hyderabad", "location": "Hyderabad", "type": "Private", "fees": 1.15, "est": 1998, "nirf": None, "website": "https://vjit.ac.in", "placement": 5.0, "tier": 4},
        {"id": "mlrit", "name": "MLR Institute of Technology (MLRIT), Dundigal", "location": "Dundigal", "type": "Private", "fees": 1.15, "est": 2005, "nirf": None, "website": "https://mlrit.ac.in", "placement": 5.8, "tier": 4},
        {"id": "mrec", "name": "Malla Reddy Engineering College (MREC), Secunderabad", "location": "Secunderabad", "type": "Private", "fees": 1.1, "est": 2002, "nirf": None, "website": "https://mrec.ac.in", "placement": 5.5, "tier": 4},
        {"id": "jbiet", "name": "JB Institute of Engineering and Technology (JBIET), Hyderabad", "location": "Hyderabad", "type": "Private", "fees": 1.05, "est": 1998, "nirf": None, "website": "https://jbiet.edu.in", "placement": 4.8, "tier": 4},
        {"id": "gnitc", "name": "Guru Nanak Institutions Technical Campus (GNITC), Ibrahimpatnam", "location": "Ibrahimpatnam", "type": "Private", "fees": 1.1, "est": 2001, "nirf": None, "website": "https://gniindia.org", "placement": 5.0, "tier": 4},
        {"id": "vits", "name": "Vignan Institute of Technology and Science (VITS), Yadadri Bhuvanagiri", "location": "Yadadri Bhuvanagiri", "type": "Private", "fees": 1.1, "est": 1999, "nirf": None, "website": "https://vignanits.ac.in", "placement": 4.8, "tier": 4},
        {"id": "mrcet", "name": "Malla Reddy College of Engineering & Technology (MRCET), Secunderabad", "location": "Secunderabad", "type": "Private", "fees": 1.1, "est": 2004, "nirf": None, "website": "https://mrcet.ac.in", "placement": 5.2, "tier": 4}
    ]

    branches = ["CSE", "ECE", "EEE", "Mechanical", "Civil"]
    
    # Facilities pool
    facilities_pool = ["Hostel", "Library", "Research Lab", "Sports", "Cafeteria", "WiFi", "Auditorium", "Gym"]

    # Seeding random state for repeatability
    random.seed(42)

    new_eamcet_entries = []
    
    # We will generate entries for all branches for all 30 colleges
    for col in colleges_def:
        tier = col["tier"]
        
        # Base closing rank for CSE based on Tier
        if tier == 1:
            base_cse = 1500
        elif tier == 2:
            base_cse = 4500
        elif tier == 3:
            base_cse = 10000
        else: # tier == 4
            base_cse = 18000

        for branch in branches:
            # Shift base closing rank according to branch popularity
            if branch == "CSE":
                branch_factor = 1.0
            elif branch == "ECE":
                branch_factor = 2.0
            elif branch == "EEE":
                branch_factor = 3.5
            elif branch == "Mechanical":
                branch_factor = 5.0
            else: # Civil
                branch_factor = 6.0

            base_closing_rank = int(base_cse * branch_factor)
            
            # Generate cutoffs for years 2024, 2023, 2022
            cutoffs = []
            
            # Categories: General, OBC, SC, ST, EWS
            categories_multipliers = {
                "General": 1.0,
                "EWS": 1.25,
                "OBC": 1.6,
                "SC": 2.8,
                "ST": 3.2
            }
            
            for year in [2024, 2023, 2022]:
                # Year multiplier (ranks change slightly year over year)
                year_mult = 1.0
                if year == 2023:
                    year_mult = 0.95 + random.uniform(-0.03, 0.03)
                elif year == 2022:
                    year_mult = 1.05 + random.uniform(-0.03, 0.03)
                else:
                    year_mult = 1.0 + random.uniform(-0.02, 0.02)
                
                for cat, cat_mult in categories_multipliers.items():
                    closing = int(base_closing_rank * cat_mult * year_mult)
                    # Add some category and branch specific variance
                    closing = int(closing * (1.0 + random.uniform(-0.05, 0.05)))
                    
                    # Ensure closing rank is at least 100
                    closing = max(100, closing)
                    
                    opening = int(closing * random.uniform(0.5, 0.75))
                    opening = max(50, opening)
                    
                    cutoffs.append({
                        "year": year,
                        "category": cat,
                        "quota": "AIQ",
                        "opening_rank": opening,
                        "closing_rank": closing
                    })

            # Facilities
            num_facilities = random.randint(4, 7)
            col_facilities = random.sample(facilities_pool, num_facilities)
            
            # Construct Entry
            entry = {
                "college_id": f"eamcet-{col['id']}-{branch.lower()}",
                "name": col["name"],
                "location": col["location"],
                "state": "Telangana",
                "exam": "EAMCET",
                "branch": branch,
                "college_type": col["type"],
                "fees_lpa": col["fees"],
                "nirf_rank": col["nirf"],
                "facilities": col_facilities,
                "website": col["website"],
                "placement_avg_lpa": col["placement"],
                "established": col["est"],
                "cutoffs": cutoffs
            }
            new_eamcet_entries.append(entry)

    # Combine preserved SVEC/Andhra with new entries
    final_eamcet_list = sved_andhra + new_eamcet_entries
    all_data["EAMCET"] = final_eamcet_list
    
    print(f"Total EAMCET college records generated: {len(new_eamcet_entries)} (30 colleges x 5 branches)")
    print(f"Total EAMCET records in updated list: {len(final_eamcet_list)}")

    # Write back to JSON
    with open(dataset_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2)
    
    print(f"Successfully wrote updated dataset back to {dataset_path}")

if __name__ == "__main__":
    generate_eamcet_colleges()
