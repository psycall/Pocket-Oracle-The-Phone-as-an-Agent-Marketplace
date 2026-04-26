"""
Orvion — Marketplace Routes
"""

import json

from fastapi import APIRouter, Depends, HTTPException

from agents import AGENT_REGISTRY
from core.memory import memory
from core.security import get_current_user
from models.schemas import AgentRegistration

router = APIRouter()


@router.get("/agents", summary="List all available agents")
async def list_agents() -> dict:
    builtin = [
        {
            "name": name,
            "description": cls().description,
            "type": "builtin",
            "version": "2.1.0",
        }
        for name, cls in AGENT_REGISTRY.items()
    ]
    return {"agents": builtin, "total": len(builtin)}


@router.get("/agents/{name}", summary="Get agent details")
async def get_agent(name: str) -> dict:
    if name not in AGENT_REGISTRY:
        raise HTTPException(404, f"Agent '{name}' not found")
    instance = AGENT_REGISTRY[name]()
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
) -> dict:
    client = await memory.client()
    payload = json.dumps(registration.model_dump())
    if hasattr(client, "set"):
        await client.set(f"marketplace:agent:{registration.name}", payload)
    return {
        "status": "registered",
        "agent": registration.name,
        "message": f"Agent '{registration.name}' is now available in the marketplace.",
    }


@router.get("/stats", summary="Marketplace statistics")
async def marketplace_stats() -> dict:
    total_executions = await memory.get_metric("total_executions")
    return {
        "total_agents": len(AGENT_REGISTRY),
        "total_executions": total_executions,
        "node": "orvion-node-001",
    }


@router.get("/pricing", summary="Public pricing catalog")
async def pricing_catalog() -> dict:
    return {
        "currency": "USDC",
        "unit": "per_request",
        "services": [
            {"key": "geoproof", "label": "GeoProof", "price": 0.0015},
            {"key": "snap_ocr", "label": "SnapOCR", "price": 0.0040},
            {"key": "human_tap", "label": "HumanTap Verify", "price": 0.0060},
        ],
    }
