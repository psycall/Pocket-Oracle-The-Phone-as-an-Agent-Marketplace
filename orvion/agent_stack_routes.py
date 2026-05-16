from fastapi import APIRouter, HTTPException, Depends
from .circle_agent_stack import agent_stack_service
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/agent-stack", tags=["Agent Stack"])

class WalletCreateRequest(BaseModel):
    agent_id: str

class TransferRequest(BaseModel):
    source_wallet_id: str
    destination_address: str
    amount: str

@router.post("/create-wallet")
async def create_wallet(request: WalletCreateRequest):
    try:
        result = agent_stack_service.create_agent_wallet(request.agent_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/balance/{wallet_id}")
async def get_balance(wallet_id: str):
    try:
        result = agent_stack_service.get_wallet_balance(wallet_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/transfer")
async def transfer(request: TransferRequest):
    try:
        result = agent_stack_service.transfer_between_agents(
            request.source_wallet_id,
            request.destination_address,
            request.amount
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
