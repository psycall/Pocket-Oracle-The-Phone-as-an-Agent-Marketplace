
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import uuid4

from orvion import models, schemas, agent_registry, settlement_engine, database
from orvion.config import settings
from auth_routes import router as auth_router
from user_management_routes import router as user_router
from settlements_history_routes import router as settlements_history_router
from dashboard_stats_routes import router as dashboard_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def on_startup():
    database.init_db()

@app.get("/health", response_model=dict)
async def health_check():
    return {"status": "healthy", "service": "ORVION", "version": settings.PROJECT_VERSION}

# Agent Registry Endpoints
@app.post(f"{settings.API_V1_STR}/discovery/agents", response_model=schemas.Agent, status_code=status.HTTP_201_CREATED)
async def register_agent(agent: schemas.AgentCreate, db: Session = Depends(get_db)):
    db_agent = agent_registry.get_agent(db, agent.agent_address) # Assuming agent_address is unique for simplicity
    if db_agent:
        raise HTTPException(status_code=400, detail="Agent already registered")
    return agent_registry.create_agent(db=db, agent=agent)

@app.get(f"{settings.API_V1_STR}/discovery/agents", response_model=List[schemas.Agent])
async def discover_agents(
    skip: int = 0,
    limit: int = 100,
    agent_type: Optional[str] = None,
    capabilities: Optional[str] = None,
    db: Session = Depends(get_db)
):
    caps_list = capabilities.split(',') if capabilities else None
    agents = agent_registry.get_agents(db, skip=skip, limit=limit, agent_type=agent_type, capabilities=caps_list)
    return agents

@app.get(f"{settings.API_V1_STR}/discovery/agents/{{agent_id}}", response_model=schemas.Agent)
async def get_agent_details(agent_id: str, db: Session = Depends(get_db)):
    agent = agent_registry.get_agent(db, agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

# Settlement Endpoints
@app.post(f"{settings.API_V1_STR}/settlement/settlements", response_model=schemas.Settlement, status_code=status.HTTP_201_CREATED)
async def create_new_settlement(settlement: schemas.SettlementCreate, db: Session = Depends(get_db)):
    return settlement_engine.create_settlement(db=db, settlement=settlement)

@app.get(f"{settings.API_V1_STR}/settlement/settlements/{{settlement_id}}", response_model=schemas.Settlement)
async def get_settlement_status(settlement_id: str, db: Session = Depends(get_db)):
    settlement = settlement_engine.get_settlement(db, settlement_id)
    if settlement is None:
        raise HTTPException(status_code=404, detail="Settlement not found")
    return settlement

@app.post(f"{settings.API_V1_STR}/settlement/execution-receipts", response_model=schemas.ExecutionReceipt, status_code=status.HTTP_201_CREATED)
async def submit_execution_receipt(receipt: schemas.ExecutionReceiptCreate, db: Session = Depends(get_db)):
    return settlement_engine.create_execution_receipt(db=db, receipt=receipt)

@app.get(f"{settings.API_V1_STR}/settlement/execution-receipts/{{receipt_id}}", response_model=schemas.ExecutionReceipt)
async def get_execution_receipt_details(receipt_id: str, db: Session = Depends(get_db)):
    receipt = settlement_engine.get_execution_receipt(db, receipt_id)
    if receipt is None:
        raise HTTPException(status_code=404, detail="Execution Receipt not found")
    return receipt

# Mock endpoint for batch settlement processing
@app.post(f"{settings.API_V1_STR}/settlement/process-batch", response_model=dict)
async def process_settlement_batch_mock(settlement_ids: List[str], db: Session = Depends(get_db)):
    settlements_to_process = []
    for s_id in settlement_ids:
        settlement = settlement_engine.get_settlement(db, s_id)
        if settlement and settlement.status == "pending":
            settlements_to_process.append(settlement)
    
    if not settlements_to_process:
        raise HTTPException(status_code=400, detail="No pending settlements found for processing")
    
    tx_hash = settlement_engine.process_settlement_batch(db, settlements_to_process)
    return {"message": "Batch processed successfully", "transaction_hash": tx_hash, "processed_count": len(settlements_to_process)}

# Include all routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(settlements_history_router)
app.include_router(dashboard_router)
