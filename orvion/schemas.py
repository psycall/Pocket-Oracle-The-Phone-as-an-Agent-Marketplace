# Copyright © 2026 ORVION. All rights reserved.
# Proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_serializer, EmailStr
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    name: str
    wallet_address: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    wallet_address: Optional[str] = None
    verified: Optional[bool] = None

class User(UserBase):
    id: str
    verified: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

    @field_serializer('created_at', 'updated_at')
    def serialize_dt(self, value: Optional[datetime]) -> Optional[str]:
        if value is None:
            return None
        return value.isoformat() if isinstance(value, datetime) else value

class UserProfile(User):
    accountAge: int
    lastUpdated: datetime

class UserStatistics(BaseModel):
    userId: str
    totalSettlements: int
    totalVolume: str
    averageSettlementTime: str
    successRate: str
    lastActivity: datetime

class UserPreferences(BaseModel):
    userId: str
    theme: str
    notifications: bool
    emailUpdates: bool
    language: str

class UserPreferencesUpdate(BaseModel):
    theme: Optional[str] = None
    notifications: Optional[bool] = None
    emailUpdates: Optional[bool] = None
    language: Optional[str] = None

# Token Schema
class Token(BaseModel):
    accessToken: str
    refreshToken: str
    expiresIn: int
    token_type: str = "bearer"

# Agent Schemas
class AgentBase(BaseModel):
    agent_address: str
    agent_name: str
    agent_type: str
    capabilities: Optional[List[str]] = None
    pricing_per_call: Optional[float] = 0.0
    endpoint_url: str
    settlement_address: str

class AgentCreate(AgentBase):
    pass

class AgentUpdate(AgentBase):
    agent_address: Optional[str] = None
    agent_name: Optional[str] = None
    agent_type: Optional[str] = None
    endpoint_url: Optional[str] = None
    settlement_address: Optional[str] = None
    is_active: Optional[bool] = None
    reputation: Optional[float] = None
    earnings: Optional[float] = None

class Agent(AgentBase):
    id: str
    is_active: bool
    reputation: float
    earnings: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
    
    @field_serializer('created_at', 'updated_at')
    def serialize_dt(self, value: Optional[datetime]) -> Optional[str]:
        if value is None:
            return None
        return value.isoformat() if isinstance(value, datetime) else value

# Job Schemas
class JobBase(BaseModel):
    agent_id: str
    description: Optional[str] = None

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: str
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
    
    @field_serializer('created_at', 'updated_at')
    def serialize_dt(self, value: Optional[datetime]) -> Optional[str]:
        if value is None:
            return None
        return value.isoformat() if isinstance(value, datetime) else value

# Settlement Schemas
class SettlementBase(BaseModel):
    agent_id: str
    job_id: str
    user_id: Optional[str] = None # Added user_id
    amount: float
    to_address: str

class SettlementCreate(SettlementBase):
    on_chain_job_id: Optional[int] = None  # ID do job no contrato Orvion on-chain

class Settlement(SettlementBase):
    id: str
    status: str
    transaction_hash: Optional[str] = None
    on_chain_job_id: Optional[int] = None  # ID do job no contrato Orvion on-chain
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
    
    @field_serializer('created_at', 'updated_at')
    def serialize_dt(self, value: Optional[datetime]) -> Optional[str]:
        if value is None:
            return None
        return value.isoformat() if isinstance(value, datetime) else value

# Execution Receipt Schemas
class ExecutionReceiptBase(BaseModel):
    job_id: str
    proof: str

class ExecutionReceiptCreate(ExecutionReceiptBase):
    pass

class ExecutionReceipt(ExecutionReceiptBase):
    id: str
    verified: bool
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
    
    @field_serializer('created_at')
    def serialize_dt(self, value: Optional[datetime]) -> Optional[str]:
        if value is None:
            return None
        return value.isoformat() if isinstance(value, datetime) else value
