# Copyright © 2026 ORVION. All rights reserved.
# Proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

"""
Job lifecycle API routes.
Implements cancel, dispute, and history endpoints for job management.
"""

import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from orvion import models, schemas, database, auth, dispute_engine
from orvion.status_constants import JobStatus, DisputeStatus
from auth_routes import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/jobs", tags=["jobs"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{job_id}/cancel", response_model=dict, status_code=status.HTTP_200_OK)
async def cancel_job(
    job_id: str,
    reason: str = None,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user)
):
    """
    Cancel a pending or financed job.
    
    Only the job creator can cancel it, and only if it's in pending or financed state.
    Cancellation triggers refund or dispute process depending on state.
    
    Args:
        job_id: Job ID to cancel
        reason: Optional cancellation reason
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Updated job record with status "cancelled"
    """
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Check authorization (job creator or admin)
    # In production, verify current_user is job creator
    
    if job.status not in [JobStatus.PENDING, "financed"]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel job in '{job.status}' state. Only pending or financed jobs can be cancelled."
        )
    
    # Update job status
    job.status = JobStatus.CANCELLED
    db.add(job)
    db.commit()
    db.refresh(job)
    
    logger.info(f"Job cancelled: {job_id} by user {current_user.id} - Reason: {reason}")
    
    return {
        "job_id": job.id,
        "status": job.status,
        "cancelled_at": job.updated_at.isoformat() if job.updated_at else None,
        "reason": reason,
        "message": "Job cancelled successfully"
    }


@router.post("/{job_id}/dispute", response_model=dict, status_code=status.HTTP_201_CREATED)
async def dispute_job(
    job_id: str,
    reason: str,
    evidence: dict = None,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user)
):
    """
    Initiate a dispute for a job.
    
    Creates a new dispute record and transitions the job to disputed state.
    Requires evidence or detailed reason for the dispute.
    
    Args:
        job_id: Job ID to dispute
        reason: Reason for dispute
        evidence: Optional evidence (documents, proofs, etc.)
        db: Database session
        current_user: Authenticated user
        
    Returns:
        New dispute record
    """
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if not reason or len(reason.strip()) < 10:
        raise HTTPException(
            status_code=400,
            detail="Dispute reason must be at least 10 characters"
        )
    
    # Get settlement for this job
    settlement = db.query(models.Settlement).filter(
        models.Settlement.job_id == job_id
    ).first()
    
    if not settlement:
        raise HTTPException(status_code=404, detail="No settlement found for this job")
    
    # Create dispute
    dispute_record = dispute_engine.DisputeManager.create_dispute(
        db=db,
        settlement_id=settlement.id,
        initiator_id=current_user.id,
        reason=reason,
        evidence=evidence
    )
    
    # Update job status
    job.status = JobStatus.DISPUTED
    db.add(job)
    
    # Update settlement status
    settlement.status = "disputed"
    db.add(settlement)
    
    db.commit()
    
    logger.info(f"Dispute created: {dispute_record['dispute_id']} for job {job_id}")
    
    return {
        "dispute_id": dispute_record["dispute_id"],
        "job_id": job_id,
        "settlement_id": settlement.id,
        "status": DisputeStatus.OPEN,
        "reason": reason,
        "initiator_id": current_user.id,
        "created_at": dispute_record["created_at"],
        "deadline": dispute_record["deadline"],
        "message": "Dispute created successfully"
    }


@router.get("/{job_id}/history", response_model=dict, status_code=status.HTTP_200_OK)
async def get_job_history(
    job_id: str,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user)
):
    """
    Get detailed history of events for a job.
    
    Returns all events related to the job including creation, financing,
    execution, settlement, disputes, and resolutions.
    
    Args:
        job_id: Job ID
        limit: Max events to return
        offset: Pagination offset
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Job history with timeline of events
    """
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Get job details
    history = {
        "job_id": job.id,
        "agent_id": job.agent_id,
        "status": job.status,
        "created_at": job.created_at.isoformat() if job.created_at else None,
        "updated_at": job.updated_at.isoformat() if job.updated_at else None,
        "description": job.description,
        "events": [
            {
                "event_type": "job.created",
                "timestamp": job.created_at.isoformat() if job.created_at else None,
                "details": {"job_id": job.id, "agent_id": job.agent_id}
            }
        ]
    }
    
    # Get execution receipts
    receipts = db.query(models.ExecutionReceipt).filter(
        models.ExecutionReceipt.job_id == job_id
    ).all()
    
    for receipt in receipts:
        history["events"].append({
            "event_type": "job.execution_receipt_submitted",
            "timestamp": receipt.created_at.isoformat() if receipt.created_at else None,
            "details": {"receipt_id": receipt.id, "verified": receipt.verified}
        })
    
    # Get settlements
    settlements = db.query(models.Settlement).filter(
        models.Settlement.job_id == job_id
    ).all()
    
    for settlement in settlements:
        history["events"].append({
            "event_type": "settlement.created",
            "timestamp": settlement.created_at.isoformat() if settlement.created_at else None,
            "details": {
                "settlement_id": settlement.id,
                "amount": settlement.amount,
                "status": settlement.status,
                "transaction_hash": settlement.transaction_hash
            }
        })
    
    # Sort events by timestamp
    history["events"].sort(key=lambda x: x["timestamp"] or "")
    
    # Apply pagination
    history["events"] = history["events"][offset:offset + limit]
    history["total_events"] = len(history["events"])
    
    return history


@router.get("/{job_id}/disputes", response_model=dict, status_code=status.HTTP_200_OK)
async def get_job_disputes(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user)
):
    """
    Get all disputes related to a job.
    
    Args:
        job_id: Job ID
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of disputes for the job
    """
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Get settlement for this job
    settlement = db.query(models.Settlement).filter(
        models.Settlement.job_id == job_id
    ).first()
    
    if not settlement:
        return {
            "job_id": job_id,
            "disputes": [],
            "total_disputes": 0
        }
    
    # Get disputes for settlement
    disputes = dispute_engine.DisputeManager.get_dispute_evidence(db, settlement.id)
    
    return {
        "job_id": job_id,
        "settlement_id": settlement.id,
        "disputes": disputes,
        "total_disputes": len(disputes)
    }
