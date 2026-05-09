
from typing import List, Optional
from uuid import uuid4
from sqlalchemy.orm import Session
from web3 import Web3

from . import models, schemas, notifications, graph_engine
from .config import settings

# Initialize Web3 provider
w3 = Web3(Web3.HTTPProvider(settings.ARC_RPC_URL))

def create_settlement(db: Session, settlement: schemas.SettlementCreate):
    db_settlement = models.Settlement(
        id=str(uuid4()),
        agent_id=settlement.agent_id,
        job_id=settlement.job_id,
        amount=settlement.amount,
        to_address=settlement.to_address,
        status="pending",
    )
    db.add(db_settlement)
    db.commit()
    db.refresh(db_settlement)
    
    # Real-time notification via WebSocket
    import asyncio
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.create_task(notifications.manager.send_personal_message(
                {"type": "settlement_created", "data": schemas.Settlement.model_validate(db_settlement).model_dump()},
                db_settlement.user_id if hasattr(db_settlement, 'user_id') else "system"
            ))
    except Exception:
        pass
        
    return db_settlement

def get_settlement(db: Session, settlement_id: str):
    return db.query(models.Settlement).filter(models.Settlement.id == settlement_id).first()

def get_agent_settlements(db: Session, agent_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.Settlement).filter(models.Settlement.agent_id == agent_id).offset(skip).limit(limit).all()

def process_settlement_batch(db: Session, settlements: List[models.Settlement]):
    # In a real scenario, this would interact with the Arc Network to batch transactions.
    # For this example, we'll just mark them as confirmed.
    transaction_hash = "0x" + uuid4().hex # Mock transaction hash
    for settlement in settlements:
        settlement.status = "confirmed"
        settlement.transaction_hash = transaction_hash
        db.add(settlement)
        
        # Update Reputation Graph (Neo4j)
        graph_engine.graph_engine.update_agent_reputation(
            agent_address=settlement.to_address,
            job_id=settlement.job_id,
            amount=float(settlement.amount),
            status="confirmed"
        )
        
        # Real-time notification via WebSocket
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(notifications.manager.send_personal_message(
                    {"type": "settlement_confirmed", "settlement_id": settlement.id, "tx_hash": transaction_hash},
                    settlement.user_id if hasattr(settlement, 'user_id') else "system"
                ))
        except Exception:
            pass
            
    db.commit()
    return transaction_hash

def create_execution_receipt(db: Session, receipt: schemas.ExecutionReceiptCreate):
    db_receipt = models.ExecutionReceipt(
        id=str(uuid4()),
        job_id=receipt.job_id,
        proof=receipt.proof,
        verified=False, # This would be verified by an oracle or smart contract
    )
    db.add(db_receipt)
    db.commit()
    db.refresh(db_receipt)
    return db_receipt

def get_execution_receipt(db: Session, receipt_id: str):
    return db.query(models.ExecutionReceipt).filter(models.ExecutionReceipt.id == receipt_id).first()
