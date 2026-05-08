
from typing import List, Optional
from pydantic import BaseModel

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

class Agent(AgentBase):
    id: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class JobBase(BaseModel):
    agent_id: str
    description: Optional[str] = None

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: str
    status: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class SettlementBase(BaseModel):
    agent_id: str
    job_id: str
    amount: float
    to_address: str

class SettlementCreate(SettlementBase):
    pass

class Settlement(SettlementBase):
    id: str
    status: str
    transaction_hash: Optional[str] = None
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class ExecutionReceiptBase(BaseModel):
    job_id: str
    proof: str

class ExecutionReceiptCreate(ExecutionReceiptBase):
    pass

class ExecutionReceipt(ExecutionReceiptBase):
    id: str
    verified: bool
    created_at: str

    class Config:
        from_attributes = True
