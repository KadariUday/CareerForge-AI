import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def check():
    url = "mongodb+srv://Samvidha_Attendance_db:Uday2006@cluster0.dve9vkg.mongodb.net/"
    client = AsyncIOMotorClient(url)
    db = client["careerforge"]
    
    pipeline = [
        {"$match": {"exam": "EAMCET_BIPC"}},
        {"$group": {"_id": "$branch", "count": {"$sum": 1}}}
    ]
    cursor = db.college_data.aggregate(pipeline)
    branches = await cursor.to_list(length=100)
    print("EAMCET_BIPC branches:")
    for b in branches:
        print(f"  {b['_id']}: {b['count']} colleges")

if __name__ == "__main__":
    asyncio.run(check())
