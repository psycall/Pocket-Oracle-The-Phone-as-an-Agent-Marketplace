from fastapi import APIRouter, HTTPException, Depends
from orvion.settlement_engine import settlement_engine
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/api/v1/settlements", tags=["Settlements"])

class AtomicSettlementRequest(BaseModel):
    settlement_id: str
    agent_wallet_id: str

class BatchSettlementRequest(BaseModel):
    requests: List[AtomicSettlementRequest]

@router.post("/process-atomic")
async def process_atomic(request: AtomicSettlementRequest):
    try:
        result = settlement_engine.process_atomic_settlement(
            request.settlement_id, 
            request.agent_wallet_id
        )
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result["message"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/process-batch")
async def process_batch(request: BatchSettlementRequest):
    """
    Endpoint de alta performance para liquidação em lote.
    """
    try:
        req_dicts = [req.dict() for req in request.requests]
        results = await settlement_engine.process_batch_settlement(req_dicts)
        return {"processed": len(results), "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health():
    return {"status": "Settlement Engine Online", "mode": "Industrial/Batch", "network": "Arc Network"}
