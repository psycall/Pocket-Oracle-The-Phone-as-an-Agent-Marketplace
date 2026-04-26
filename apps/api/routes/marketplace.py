"""
Orvion — Marketplace Routes
The agent marketplace — register, discover, and use agents.
GET  /marketplace/agents          → list all agents
GET  /marketplace/agents/{name}   → agent details
POST /marketplace/agents/register → register a new agent
"""

from fastapi import APIRouter, Depends, HTTPException
from agents import AGENT_REGISTRY
from core.security import get_current_user
from models.schemas import AgentRegistration
from core.memory import memory
import json

router = APIRouter()


@router.get("/agents", summary="List all available agents")
async def list_agents():
    """
    Returns all agents registered in this node.
    No auth required — public catalog.
    """
    builtin = [
        {
            "name": name,
            "description": cls().description,
            "type": "builtin",
            "version": "2.0.0",
        }
        for name, cls in AGENT_REGISTRY.items()
    ]
    return {"agents": builtin, "total": len(builtin)}


@router.get("/agents/{name}", summary="Get agent details")
async def get_agent(name: str):
    if name not in AGENT_REGISTRY:
        raise HTTPException(404, f"Agent '{name}' not found")
    cls = AGENT_REGISTRY[name]
    instance = cls()
    return {
        "name": instance.name,
        "description": instance.description,
        "type": "builtin",
        "capabilities": ["execute", "stream"],
    }


@router.post("/agents/register", summary="Register an external agent")
async def register_agent(
    registration: AgentRegistration,
    _user: dict = Depends(get_current_user),
):
    """
    Register an external agent into the Orvion marketplace.
    Once registered, it can be discovered and called by the execution engine.
    """
    client = await memory.client()
    key = f"marketplace:agent:{registration.name}"
    await client.set(key, json.dumps(registration.model_dump()))
    return {
        "status": "registered",
        "agent": registration.name,
        "message": f"Agent '{registration.name}' is now available in the marketplace.",
    }


@router.get("/stats", summary="Marketplace statistics")
async def marketplace_stats():
    total_executions = await memory.get_metric("total_executions")
    return {
        "total_agents": len(AGENT_REGISTRY),
        "total_executions": total_executions,
        "node": "orvion-node-001",
    }
