"""
Circle Agent Stack Routes
Agent Wallets, Marketplace, Nanopayments, and Skills
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from decimal import Decimal
from orvion.agent_stack_full import (
    get_agent_stack,
    AgentRole,
    SkillCategory,
)

router = APIRouter(prefix="/api/v1/agent-stack", tags=["Agent Stack"])

# Request/Response Models
class CreateWalletRequest(BaseModel):
    agent_id: str
    wallet_address: str
    initial_balance: float = 0.0

class FundWalletRequest(BaseModel):
    agent_id: str
    amount: float = Field(..., gt=0)

class RegisterServiceRequest(BaseModel):
    provider_agent_id: str
    name: str
    description: str
    category: str
    price_per_call: float = Field(..., gt=0)

class CreateNanopaymentRequest(BaseModel):
    from_agent_id: str
    to_agent_id: str
    service_id: str
    amount: float = Field(..., gt=0)
    metadata: Optional[dict] = None

class ConfirmNanopaymentRequest(BaseModel):
    payment_id: str
    tx_hash: str

class RateServiceRequest(BaseModel):
    service_id: str
    rating: float = Field(..., ge=1, le=5)

class RegisterSkillRequest(BaseModel):
    name: str
    category: str
    description: str

class EnableSkillRequest(BaseModel):
    skill_id: str
    agent_id: str

# ============ Agent Wallets ============

@router.post("/wallets/create")
async def create_wallet(request: CreateWalletRequest):
    """Create a new agent wallet"""
    try:
        stack = get_agent_stack()
        wallet = await stack.create_agent_wallet(
            request.agent_id,
            request.wallet_address,
            Decimal(str(request.initial_balance)),
        )
        return wallet.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/wallets/{agent_id}")
async def get_wallet(agent_id: str):
    """Get agent wallet details"""
    try:
        stack = get_agent_stack()
        wallet = await stack.get_agent_wallet(agent_id)
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")
        return wallet.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/wallets/fund")
async def fund_wallet(request: FundWalletRequest):
    """Fund an agent wallet"""
    try:
        stack = get_agent_stack()
        result = await stack.fund_agent_wallet(
            request.agent_id,
            Decimal(str(request.amount)),
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/wallets/{agent_id}/balance")
async def get_balance(agent_id: str):
    """Get agent wallet balance"""
    try:
        stack = get_agent_stack()
        balance = await stack.get_wallet_balance(agent_id)
        return {"agent_id": agent_id, "balance_usdc": float(balance)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ Agent Marketplace ============

@router.post("/marketplace/services/register")
async def register_service(request: RegisterServiceRequest):
    """Register a service in the marketplace"""
    try:
        stack = get_agent_stack()
        category = SkillCategory(request.category.lower())
        service = await stack.register_service(
            request.provider_agent_id,
            request.name,
            request.description,
            category,
            Decimal(str(request.price_per_call)),
        )
        return service.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/marketplace/services")
async def discover_services(
    category: Optional[str] = Query(None),
    min_rating: float = Query(0.0, ge=0, le=5),
):
    """Discover services in marketplace"""
    try:
        stack = get_agent_stack()
        skill_category = SkillCategory(category.lower()) if category else None
        services = await stack.discover_services(skill_category, min_rating)
        return [s.to_dict() for s in services]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/marketplace/services/{service_id}")
async def get_service(service_id: str):
    """Get service details"""
    try:
        stack = get_agent_stack()
        service = await stack.get_service(service_id)
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        return service.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/marketplace/services/rate")
async def rate_service(request: RateServiceRequest):
    """Rate a service"""
    try:
        stack = get_agent_stack()
        result = await stack.rate_service(request.service_id, request.rating)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ Nanopayments ============

@router.post("/nanopayments/create")
async def create_nanopayment(request: CreateNanopaymentRequest):
    """Create a nanopayment"""
    try:
        stack = get_agent_stack()
        payment = await stack.create_nanopayment(
            request.from_agent_id,
            request.to_agent_id,
            request.service_id,
            Decimal(str(request.amount)),
            request.metadata,
        )
        return payment.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/nanopayments/confirm")
async def confirm_nanopayment(request: ConfirmNanopaymentRequest):
    """Confirm a nanopayment on-chain"""
    try:
        stack = get_agent_stack()
        result = await stack.confirm_nanopayment(
            request.payment_id,
            request.tx_hash,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/nanopayments/{payment_id}")
async def get_nanopayment(payment_id: str):
    """Get nanopayment details"""
    try:
        stack = get_agent_stack()
        payment = await stack.get_nanopayment(payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        return payment.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ Circle Skills ============

@router.post("/skills/register")
async def register_skill(request: RegisterSkillRequest):
    """Register a Circle Skill"""
    try:
        stack = get_agent_stack()
        category = SkillCategory(request.category.lower())
        skill = await stack.register_skill(
            request.name,
            category,
            request.description,
        )
        return skill.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/skills/enable")
async def enable_skill(request: EnableSkillRequest):
    """Enable a skill for an agent"""
    try:
        stack = get_agent_stack()
        result = await stack.enable_skill_for_agent(
            request.skill_id,
            request.agent_id,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/skills/agent/{agent_id}")
async def get_agent_skills(agent_id: str):
    """Get skills enabled for an agent"""
    try:
        stack = get_agent_stack()
        skills = await stack.get_agent_skills(agent_id)
        return [s.to_dict() for s in skills]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ Analytics ============

@router.get("/stats/agent/{agent_id}")
async def get_agent_stats(agent_id: str):
    """Get agent statistics"""
    try:
        stack = get_agent_stack()
        stats = await stack.get_agent_stats(agent_id)
        return stats
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/marketplace")
async def get_marketplace_stats():
    """Get marketplace statistics"""
    try:
        stack = get_agent_stack()
        stats = await stack.get_marketplace_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/transactions/history")
async def get_transaction_history(limit: int = Query(100, ge=1, le=1000)):
    """Get transaction history"""
    try:
        stack = get_agent_stack()
        history = await stack.get_transaction_history(limit)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check for Agent Stack"""
    try:
        stack = get_agent_stack()
        stats = await stack.get_marketplace_stats()
        return {
            "status": "healthy",
            "service": "Circle Agent Stack",
            "marketplace": stats,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
