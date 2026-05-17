import os
import json
import httpx
import asyncio
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import local modules
import sys
sys.path.append(os.getcwd())
from orvion import models, database

BASE_URL = "http://127.0.0.1:8000"

async def test_api_health():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        print("✅ API Health Check: PASSED")

async def test_database_integrity():
    engine = create_engine("sqlite:///./orvion.db")
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        # Check if tables exist
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        expected_tables = ["users", "agents", "jobs", "settlements"]
        for table in expected_tables:
            assert table in tables
        print(f"✅ Database Integrity: PASSED (Tables: {', '.join(tables)})")
    finally:
        db.close()

async def run_all_tests():
    print("🚀 Starting ORVION Full Integration Tests...")
    
    # Start server in background if not running
    # (Assuming server is managed externally for this test script)
    
    try:
        await test_api_health()
        await test_database_integrity()
        print("\n🎉 All critical systems are OPERATIONAL.")
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run_all_tests())
