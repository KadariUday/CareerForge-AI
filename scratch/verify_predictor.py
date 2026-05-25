import asyncio
import httpx

async def verify():
    url = "http://localhost:8000/api/college/predict"
    payload = {
        "exam": "EAMCET_BIPC",
        "rank": 15000,
        "category": "OBC",
        "state": "Telangana",
        "preferred_branch": "Agriculture"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, timeout=10.0)
            if response.status_code == 200:
                data = response.json()
                print(f"Total found: {data.get('total_found')}")
                for category in ['safe', 'target', 'dream']:
                    colleges = data.get(category, [])
                    print(f"\n--- {category.upper()} ({len(colleges)}) ---")
                    for c in colleges:
                        print(f"{c['college']['name']} | {c['college']['branch']} | Chance: {c['admission_chance_percent']}%")
            else:
                print(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(verify())
