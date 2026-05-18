"""
SQLAlchemy models for the Legal Body module.

Designed to coexist with ORVION's existing SQLAlchemy `Base` —
import this module from your `main.py` so the tables are registered.
"""
from __future__ import annotations
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, Enum, JSON, Boolean
)
from sqlalchemy.orm import relationship
import enum
from orvion.models import Base


class JurisdictionEnum(str, enum.Enum):
    WYOMING_DAO_LLC = "WYOMING_DAO_LLC"
    DELAWARE_SERIES_LLC = "DELAWARE_SERIES_LLC"
    NEW_YORK_LLC = "NEW_YORK_LLC"
    MARSHALL_ISLANDS_DAO = "MARSHALL_ISLANDS_DAO"


class PersonaStatus(str, enum.Enum):
    PENDING = "PENDING"
    INCORPORATED = "INCORPORATED"
    SUSPENDED = "SUSPENDED"
    DISSOLVED = "DISSOLVED"


class AgentPersona(Base):
    __tablename__ = "agent_personas"

    id = Column(Integer, primary_key=True, index=True)
    on_chain_id = Column(Integer, nullable=True, index=True)
    agent_wallet = Column(String(42), nullable=False, unique=True, index=True)
    human_sponsor = Column(String(42), nullable=True)
    jurisdiction = Column(Enum(JurisdictionEnum), nullable=False)
    status = Column(Enum(PersonaStatus), default=PersonaStatus.PENDING, nullable=False)
    legal_name = Column(String(255), nullable=False)
    operating_agreement_hash = Column(String(66), nullable=True)
    operating_agreement_uri = Column(String(512), nullable=True)
    registered_agent_uri = Column(String(512), nullable=True)
    ein = Column(String(20), nullable=True)
    extra = Column(JSON, default=dict)

    incorporated_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    signers = relationship("PersonaSigner", back_populates="persona", cascade="all, delete-orphan")


class PersonaSigner(Base):
    __tablename__ = "persona_signers"

    id = Column(Integer, primary_key=True)
    persona_id = Column(Integer, ForeignKey("agent_personas.id", ondelete="CASCADE"))
    signer_address = Column(String(42), nullable=False)
    role = Column(String(50), default="signer")  # signer | manager | counsel | registered_agent
    is_active = Column(Boolean, default=True)
    added_at = Column(DateTime, default=datetime.utcnow)

    persona = relationship("AgentPersona", back_populates="signers")
