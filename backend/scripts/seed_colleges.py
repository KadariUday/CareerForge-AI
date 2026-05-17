import json
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import sys
import os

# Add parent directory to path to import settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import settings

async def seed_colleges():
    print(f"Connecting to MongoDB at {settings.MONGODB_URL}...")
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    collection = db.college_data

    # Load data from JSON files
    db_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "database")
    neet_path = os.path.join(db_dir, "neet_full_dataset.json")
    college_path = os.path.join(db_dir, "college_data.json")
    all_exams_path = os.path.join(db_dir, "all_exam_datasets.json")
    
    data = []
    
    # 1. Load NEET Full Dataset
    if os.path.exists(neet_path):
        print(f"Loading NEET data from {neet_path}...")
        try:
            with open(neet_path, 'r', encoding='utf-8') as f:
                data.extend(json.load(f))
        except Exception as e:
            print(f"Error loading {neet_path}: {e}")
    
    # 2. Load All Exam Datasets (Dict structure)
    if os.path.exists(all_exams_path):
        print(f"Loading all exam datasets from {all_exams_path}...")
        try:
            with open(all_exams_path, 'r', encoding='utf-8') as f:
                exams_data = json.load(f)
                if isinstance(exams_data, dict):
                    for exam_name, colleges in exams_data.items():
                        print(f"  - Adding {len(colleges)} colleges for {exam_name}")
                        data.extend(colleges)
                elif isinstance(exams_data, list):
                    data.extend(exams_data)
        except Exception as e:
            print(f"Error loading {all_exams_path}: {e}")

    # 3. Load Additional/Legacy College Data
    if os.path.exists(college_path):
        print(f"Loading additional data from {college_path}...")
        try:
            with open(college_path, 'r', encoding='utf-8') as f:
                other_data = json.load(f)
                # Transform old flat structure to new nested structure for compatibility
                for item in other_data:
                    if "cutoffs" not in item:
                        item["cutoffs"] = [{
                            "year": 2024,
                            "category": item.get("category", "General"),
                            "closing_rank": item.get("cutoff_rank", 0),
                            "quota": "AIQ"
                        }]
                    data.append(item)
        except Exception as e:
            print(f"Error loading {college_path}: {e}")

    if not data:
        print("Error: No data found in JSON files")
        client.close()
        return

    # Deduplication and normalization
    print("Normalizing and deduplicating data...")
    unique_data = {}
    for item in data:
        # Generate a unique key
        cid = item.get("college_id")
        name = item.get("name", "Unknown")
        branch = item.get("branch", "N/A")
        exam = item.get("exam", "UNKNOWN")
        
        key = cid if cid else f"{name}-{branch}-{exam}".lower().replace(" ", "")
        
        # Ensure required fields exist for the model
        item["exam"] = item.get("exam", "UNKNOWN").upper()
        if item.get("state") == "India":
            item["state"] = "All India"
            
        if "college_id" not in item:
            item["college_id"] = key
            
        unique_data[key] = item
    
    final_data = list(unique_data.values())
    print(f"Total unique records to insert: {len(final_data)}")

    # Clear existing data (optional, but good for clean seed)
    print(f"Clearing existing data in {collection.name}...")
    await collection.delete_many({})

    # Insert data
    print(f"Inserting {len(final_data)} colleges into MongoDB...")
    if final_data:
        result = await collection.insert_many(final_data)
        print(f"Successfully inserted {len(result.inserted_ids)} records.")
    
    # Create indexes
    print("Creating/Verifying indexes...")
    await collection.create_index([("exam", 1), ("state", 1)])
    await collection.create_index("cutoffs.category")
    await collection.create_index("fees_lpa")
    await collection.create_index("college_id", unique=True)
    
    print("Seeding complete!")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_colleges())
