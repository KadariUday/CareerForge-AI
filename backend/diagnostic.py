"""
CareerForge AI — Startup Diagnostic Wrapper
Catches and logs any low-level import, Pydantic, or runtime errors during boot.
"""
import os
import sys
import traceback

print("==================================================")
print("[INFO] CAREERFORGE BACKEND DIAGNOSTIC BOOT SEQUENCE")
print("==================================================")
print(f"Python Version : {sys.version}")
print(f"Platform       : {sys.platform}")
print(f"Working Dir    : {os.getcwd()}")
print(f"Python Path    : {sys.path}")
print("==================================================")

try:
    print("Step 1: Testing settings module import...")
    from config.settings import settings
    print("Settings imported successfully!")
    
    print("\nStep 2: Testing database module import...")
    from config.database import connect_db
    print("Database connection helper imported!")
    
    print("\nStep 3: Testing FastAPI application entry point import...")
    import main
    print("Entry point 'main' imported successfully!")
    
    print("\nStep 4: Starting Uvicorn Server...")
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"Binding to host 0.0.0.0 on port {port}...")
    
    # Run with 1 worker, no reload for stable production
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        workers=1
    )
    
except Exception as e:
    print("\nCRITICAL STARTUP ERROR DETECTED!")
    print("==================================================")
    traceback.print_exc(file=sys.stdout)
    print("==================================================")
    sys.exit(1)
