"""
Orvion — API Schemas
All request/response models using Pydantic v2.
"""

from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime


# ── Requests ─────────────────────────────────────────────────

class TaskRequest(BaseModel):
    goal: str = Field(..., min_length=3, max_length=1000, description="Natural language goal to execute")
    context: dict = Field(default_factory=dict, description="Optional context for the agent")

    model_config = {
        "json_schema_extra": {
            "example": {
                "goal": "Analyze crypto trends and find the best opportunity",
                "context": {"risk_tolerance": "medium", "portfolio_size": "10000"},
            }
        }
    }


class TokenRequest(BaseModel):
    api_key: str = Field(..., description="Your Orvion API key")


class AgentRegistration(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    description: str
    endpoint: str = Field(..., description="URL where this agent can be reached")
    capabilities: list[str] = Field(default_factory=list)
    version: str = "1.0.0"


# ── Responses ────────────────────────────────────────────────

class TaskRecord(BaseModel):
    id: str
    node: str
    goal: str
    agent_used: str
    result: dict
    duration_ms: int
    timestamp: float
    status: str


class NodeStatus(BaseModel):
    node_id: str
    version: str
    status: str
    environment: str
    tasks_executed: int
    uptime_seconds: float


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class HealthResponse(BaseModel):
    status: str
    node: str
    timestamp: str
