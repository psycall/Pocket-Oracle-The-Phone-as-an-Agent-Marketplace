
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .auth import User # Import User model

Base = declarative_base()

class Agent(Base):
    __tablename__ = "agents"

    id = Column(String, primary_key=True, index=True)
    agent_address = Column(String, unique=True, index=True, nullable=False)
    agent_name = Column(String, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    reputation = Column(Float, default=0.0)
    earnings = Column(Float, default=0.0)
    agent_type = Column(String, nullable=False)
    capabilities = Column(String) # Stored as comma-separated string for simplicity
    pricing_per_call = Column(Float, default=0.0)
    endpoint_url = Column(String, nullable=False)
    settlement_address = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    jobs = relationship("Job", back_populates="agent")
    settlements = relationship("Settlement", back_populates="agent")

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False)
    status = Column(String, default="pending")
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    agent = relationship("Agent", back_populates="jobs")
    execution_receipts = relationship("ExecutionReceipt", back_populates="job")

class Settlement(Base):
    __tablename__ = "settlements"

    id = Column(String, primary_key=True, index=True)
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False)
    job_id = Column(String, ForeignKey("jobs.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=True) # Added for user-specific settlement history
    amount = Column(Float, nullable=False)
    to_address = Column(String, nullable=False)
    status = Column(String, default="pending") # pending, confirmed, failed
    transaction_hash = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    agent = relationship("Agent", back_populates="settlements")
    job = relationship("Job")
    user = relationship("User")

class ExecutionReceipt(Base):
    __tablename__ = "execution_receipts"

    id = Column(String, primary_key=True, index=True)
    job_id = Column(String, ForeignKey("jobs.id"), nullable=False)
    proof = Column(String, nullable=False)
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    job = relationship("Job", back_populates="execution_receipts")

# Additional models (Reputation, Orchestration, etc.) can be added here as needed
