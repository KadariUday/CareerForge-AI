import asyncio
import motor.motor_asyncio
from backend.config.settings import settings

async def check():
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    colleges = await db.college_data.count_documents({})
    users = await db.users.count_documents({})
    print(f"Colleges count: {colleges}")
    print(f"Users count: {users}")

if __name__ == "__main__":
    asyncio.run(check())
