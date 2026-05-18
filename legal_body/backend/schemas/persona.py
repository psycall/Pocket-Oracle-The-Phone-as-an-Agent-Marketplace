"""Pydantic schemas for the Legal Body API."""
from __future__ import annotations
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from ..models.persona import JurisdictionEnum, PersonaStatus


class IncorporateRequest(BaseModel):
    agent_wallet: str = Field(..., pattern=r"^0x[a-fA-F0-9]{40}$")
    legal_name: str = Field(..., min_length=3, max_length=255)
    jurisdiction: JurisdictionEnum
    human_sponsor: Optional[str] = Field(None, pattern=r"^0x[a-fA-F0-9]{40}$")
    registered_agent_uri: Optional[str] = None
    purpose: Optional[str] = "Lawful business activities including but not limited to autonomous AI-driven commerce, agent-to-agent settlement, and on-chain asset management."
    initial_capital_usdc: float = 0.0


class SignAgreementRequest(BaseModel):
    persona_id: int
    document_hash: str = Field(..., pattern=r"^0x[a-fA-F0-9]{64}$")
    document_uri: str
    signature: Optional[str] = None  # EIP-712 / ERC-1271


class DissociateRequest(BaseModel):
    persona_id: int
    reason: str = "Transition to zero-member configuration per Bayern model"


class PersonaResponse(BaseModel):
    id: int
    on_chain_id: Optional[int]
    agent_wallet: str
    human_sponsor: Optional[str]
    jurisdiction: JurisdictionEnum
    status: PersonaStatus
    legal_name: str
    operating_agreement_hash: Optional[str]
    operating_agreement_uri: Optional[str]
    registered_agent_uri: Optional[str]
    ein: Optional[str]
    incorporated_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class PersonaListResponse(BaseModel):
    total: int
    items: List[PersonaResponse]
