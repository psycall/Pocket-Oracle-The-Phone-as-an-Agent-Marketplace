"""
Database initialization script
Creates tables and seeds initial data
"""

import asyncio
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Import models
from orvion.models import Base, User, Agent, Settlement, ExecutionReceipt
from orvion.database import get_db

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://user:password@localhost/orvion"
)


def init_database():
    """Initialize database with tables"""
    logger.info("🔧 Initializing database...")

    engine = create_engine(DATABASE_URL, echo=False)

    # Create tables
    logger.info("📝 Creating tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Tables created successfully")

    # Seed initial data
    logger.info("🌱 Seeding initial data...")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # Check if data already exists
        existing_users = db.query(User).count()
        if existing_users > 0:
            logger.info("📊 Database already seeded. Skipping...")
            return

        # Create admin user
        admin_user = User(
            username="admin",
            email="admin@orvion.io",
            full_name="Admin User",
            hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUFutQFm",  # password
            is_active=True,
            is_admin=True,
        )
        db.add(admin_user)

        # Create demo agent
        demo_agent = Agent(
            agent_address="0x1234567890123456789012345678901234567890",
            agent_name="DemoAgent-01",
            agent_type="processor",
            capabilities=["data_processing", "validation"],
            pricing_per_call=0.5,
            reputation_score=4.8,
            total_jobs=150,
            success_rate=0.98,
        )
        db.add(demo_agent)

        db.commit()
        logger.info("✅ Initial data seeded successfully")

        # Log summary
        users_count = db.query(User).count()
        agents_count = db.query(Agent).count()
        logger.info(f"📊 Database summary: {users_count} users, {agents_count} agents")

    except Exception as e:
        logger.error(f"❌ Error seeding data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

    logger.info("🎉 Database initialization complete!")


if __name__ == "__main__":
    init_database()
