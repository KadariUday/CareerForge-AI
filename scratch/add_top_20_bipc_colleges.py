import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def seed_top_20():
    url = "mongodb+srv://Samvidha_Attendance_db:Uday2006@cluster0.dve9vkg.mongodb.net/"
    client = AsyncIOMotorClient(url)
    db = client["careerforge"]
    collection = db.college_data
    
    top_colleges = [
        # Veterinary Colleges (PVNRTVU - Telangana)
        {
            "college_id": "vet-rajendranagar",
            "name": "College of Veterinary Science, Rajendranagar (PVNRTVU)",
            "location": "Hyderabad",
            "state": "Telangana",
            "exam": "EAMCET_BIPC",
            "branch": "B.V.Sc & A.H.",
            "college_type": "Government",
            "fees_lpa": 0.4,
            "nirf_rank": 45,
            "facilities": ["Hospital", "Farm", "Hostel", "Library"],
            "cutoffs": [
                {"year": 2024, "category": "General", "closing_rank": 850, "quota": "SQ"},
                {"year": 2024, "category": "OBC", "closing_rank": 1400, "quota": "SQ"},
                {"year": 2024, "category": "SC", "closing_rank": 2900, "quota": "SQ"},
                {"year": 2024, "category": "ST", "closing_rank": 3500, "quota": "SQ"},
                {"year": 2024, "category": "EWS", "closing_rank": 1100, "quota": "SQ"}
            ]
        },
        {
            "college_id": "vet-korutla",
            "name": "College of Veterinary Science, Korutla (PVNRTVU)",
            "location": "Korutla",
            "state": "Telangana",
            "exam": "EAMCET_BIPC",
            "branch": "B.V.Sc & A.H.",
            "college_type": "Government",
            "fees_lpa": 0.4,
            "cutoffs": [
                {"year": 2024, "category": "General", "closing_rank": 1200, "quota": "SQ"},
                {"year": 2024, "category": "OBC", "closing_rank": 2100, "quota": "SQ"},
                {"year": 2024, "category": "SC", "closing_rank": 4200, "quota": "SQ"},
                {"year": 2024, "category": "ST", "closing_rank": 4900, "quota": "SQ"}
            ]
        },
        {
            "college_id": "vet-mamnoor",
            "name": "College of Veterinary Science, Mamnoor (PVNRTVU)",
            "location": "Warangal",
            "state": "Telangana",
            "exam": "EAMCET_BIPC",
            "branch": "B.V.Sc & A.H.",
            "college_type": "Government",
            "fees_lpa": 0.4,
            "cutoffs": [
                {"year": 2024, "category": "General", "closing_rank": 1500, "quota": "SQ"},
                {"year": 2024, "category": "OBC", "closing_rank": 2500, "quota": "SQ"},
                {"year": 2024, "category": "SC", "closing_rank": 4800, "quota": "SQ"}
            ]
        },
        # Veterinary Colleges (SVVU - Andhra Pradesh)
        {
            "college_id": "vet-tirupati",
            "name": "College of Veterinary Science, Tirupati (SVVU)",
            "location": "Tirupati",
            "state": "Andhra Pradesh",
            "exam": "EAMCET_BIPC",
            "branch": "B.V.Sc & A.H.",
            "college_type": "Government",
            "fees_lpa": 0.45,
            "cutoffs": [
                {"year": 2024, "category": "General", "closing_rank": 950, "quota": "SQ"},
                {"year": 2024, "category": "OBC", "closing_rank": 1600, "quota": "SQ"},
                {"year": 2024, "category": "SC", "closing_rank": 3100, "quota": "SQ"}
            ]
        },
        {
            "college_id": "vet-gannavaram",
            "name": "NTR College of Veterinary Science, Gannavaram (SVVU)",
            "location": "Vijayawada",
            "state": "Andhra Pradesh",
            "exam": "EAMCET_BIPC",
            "branch": "B.V.Sc & A.H.",
            "college_type": "Government",
            "fees_lpa": 0.45,
            "cutoffs": [
                {"year": 2024, "category": "General", "closing_rank": 1100, "quota": "SQ"},
                {"year": 2024, "category": "OBC", "closing_rank": 1800, "quota": "SQ"}
            ]
        },
        {
            "college_id": "vet-proddatur",
            "name": "College of Veterinary Science, Proddatur (SVVU)",
            "location": "Kadapa",
            "state": "Andhra Pradesh",
            "exam": "EAMCET_BIPC",
            "branch": "B.V.Sc & A.H.",
            "college_type": "Government",
            "fees_lpa": 0.45,
            "cutoffs": [
                {"year": 2024, "category": "General", "closing_rank": 1400, "quota": "SQ"},
                {"year": 2024, "category": "OBC", "closing_rank": 2200, "quota": "SQ"}
            ]
        },
        {
            "college_id": "vet-garividi",
            "name": "College of Veterinary Science, Garividi (SVVU)",
            "location": "Vizianagaram",
            "state": "Andhra Pradesh",
            "exam": "EAMCET_BIPC",
            "branch": "B.V.Sc & A.H.",
            "college_type": "Government",
            "fees_lpa": 0.45,
            "cutoffs": [
                {"year": 2024, "category": "General", "closing_rank": 1600, "quota": "SQ"},
                {"year": 2024, "category": "OBC", "closing_rank": 2600, "quota": "SQ"}
            ]
        },
        # Add 3 Top Pharmacy Colleges for EAMCET BIPC
        {
            "college_id": "pharm-ou",
            "name": "University College of Technology (Pharmacy), OU",
            "location": "Hyderabad",
            "state": "Telangana",
            "exam": "EAMCET_BIPC",
            "branch": "B.Pharmacy",
            "college_type": "Government",
            "fees_lpa": 0.35,
            "cutoffs": [
                {"year": 2024, "category": "General", "closing_rank": 3200, "quota": "SQ"},
                {"year": 2024, "category": "OBC", "closing_rank": 5400, "quota": "SQ"}
            ]
        },
        {
            "college_id": "pharm-au",
            "name": "AU College of Pharmaceutical Sciences",
            "location": "Visakhapatnam",
            "state": "Andhra Pradesh",
            "exam": "EAMCET_BIPC",
            "branch": "B.Pharmacy",
            "college_type": "Government",
            "fees_lpa": 0.40,
            "cutoffs": [
                {"year": 2024, "category": "General", "closing_rank": 3500, "quota": "SQ"},
                {"year": 2024, "category": "OBC", "closing_rank": 5800, "quota": "SQ"}
            ]
        },
        {
            "college_id": "pharm-kakatiya",
            "name": "University College of Pharmaceutical Sciences, KU",
            "location": "Warangal",
            "state": "Telangana",
            "exam": "EAMCET_BIPC",
            "branch": "B.Pharmacy",
            "college_type": "Government",
            "fees_lpa": 0.30,
            "cutoffs": [
                {"year": 2024, "category": "General", "closing_rank": 4100, "quota": "SQ"},
                {"year": 2024, "category": "OBC", "closing_rank": 6200, "quota": "SQ"}
            ]
        }
    ]

    print(f"Adding {len(top_colleges)} top BIPC colleges to MongoDB...")
    
    for college in top_colleges:
        # Use update_one with upsert to avoid duplicate key errors
        await collection.update_one(
            {"college_id": college["college_id"]},
            {"$set": college},
            upsert=True
        )
        
    print("Database seeding executed successfully.")

if __name__ == "__main__":
    asyncio.run(seed_top_20())
