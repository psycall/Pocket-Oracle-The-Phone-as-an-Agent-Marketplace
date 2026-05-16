# Copyright © 2026 ORVION. All rights reserved.
# Proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

"""
Dispute management API routes.
Implements dispute creation, evidence submission, and resolution endpoints.
"""

import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from orvion import models, database, auth
from orvion.dispute_engine import DisputeManager, ArbitrationEngine
from auth_routes import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/disputes", tags=["disputes"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic models
class EvidenceSubmission(BaseModel):
    evidence_type: str  # "document", "proof", "screenshot", etc.
    content: str  # Base64-encoded or URL
    description: Optional[str] = None


class DisputeResolution(BaseModel):
    resolution: str  # "settlement_upheld" or "settlement_reversed"
    ruling: str
    notes: Optional[str] = None


class DisputeAppeal(BaseModel):
    appeal_reason: str


@router.get("", response_model=dict, status_code=status.HTTP_200_OK)
async def list_disputes(
    status_filter: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user)
):
    """
    List all disputes (admin/arbitrator only).
    
    Args:
        status_filter: Optional status filter (open, in_review, resolved, closed, appealed)
        limit: Max disputes to return
        offset: Pagination offset
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of disputes
    """
    # Get open disputes
    disputes = DisputeManager.get_open_disputes(db, limit, offset)
    
    return {
        "disputes": disputes,
        "total_disputes": len(disputes),
        "limit": limit,
        "offset": offset,
        "filters": {"status": status_filter}
    }


@router.get("/{dispute_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def get_dispute(
    dispute_id: str,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user)
):
    """
    Get details of a specific dispute.
    
    Args:
        dispute_id: Dispute ID
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Dispute details
    """
    dispute = DisputeManager.get_dispute(db, dispute_id)
    
    if not dispute:
        raise HTTPException(status_code=404, detail="Dispute not found")
    
    return dispute


@router.post("/{dispute_id}/evidence", response_model=dict, status_code=status.HTTP_201_CREATED)
async def submit_evidence(
    dispute_id: str,
    evidence: EvidenceSubmission,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user)
):
    """
    Submit evidence for a dispute.
    
    Parties involved in a dispute can submit evidence to support their case.
    Evidence must be submitted before the evidence deadline.
    
    Args:
        dispute_id: Dispute ID
        evidence: Evidence data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Evidence record
    """
    dispute = DisputeManager.get_dispute(db, dispute_id)
    
    if not dispute:
        raise HTTPException(status_code=404, detail="Dispute not found")
    
    # Submit evidence
    evidence_record = DisputeManager.submit_evidence(
        db=db,
        dispute_id=dispute_id,
        submitter_id=current_user.id,
        evidence={
            "type": evidence.evidence_type,
            "content": evidence.content,
            "description": evidence.description
        }
    )
    
    logger.info(f"Evidence submitted for dispute {dispute_id} by {current_user.id}")
    
    return {
        "evidence_id": evidence_record["evidence_id"],
        "dispute_id": dispute_id,
        "evidence_type": evidence.evidence_type,
        "submitted_at": evidence_record["submitted_at"],
        "message": "Evidence submitted successfully"
    }


@router.get("/{dispute_id}/evidence", response_model=dict, status_code=status.HTTP_200_OK)
async def get_dispute_evidence(
    dispute_id: str,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user)
):
    """
    Get all evidence for a dispute.
    
    Args:
        dispute_id: Dispute ID
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of evidence records
    """
    dispute = DisputeManager.get_dispute(db, dispute_id)
    
    if not dispute:
        raise HTTPException(status_code=404, detail="Dispute not found")
    
    evidence_list = DisputeManager.get_dispute_evidence(db, dispute_id)
    
    return {
        "dispute_id": dispute_id,
        "evidence": evidence_list,
        "total_evidence": len(evidence_list)
    }


@router.post("/{dispute_id}/analysis", response_model=dict, status_code=status.HTTP_200_OK)
async def analyze_dispute(
    dispute_id: str,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user)
):
    """
    Analyze a dispute and generate preliminary assessment.
    
    Requires arbitrator/admin role. Generates analysis and recommendation
    based on available evidence.
    
    Args:
        dispute_id: Dispute ID
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Analysis and recommendation
    """
    dispute = DisputeManager.get_dispute(db, dispute_id)
    
    if not dispute:
        raise HTTPException(status_code=404, detail="Dispute not found")
    
    # Analyze dispute
    analysis = ArbitrationEngine.analyze_dispute(db, dispute_id)
    
    logger.info(f"Dispute analyzed: {dispute_id}")
    
    return analysis


@router.post("/{dispute_id}/resolve", response_model=dict, status_code=status.HTTP_200_OK)
async def resolve_dispute(
    dispute_id: str,
    resolution: DisputeResolution,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user)
):
    """
    Resolve a dispute with a ruling.
    
    Requires arbitrator/admin role. Finalizes the dispute with a resolution.
    
    Args:
        dispute_id: Dispute ID
        resolution: Resolution details
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Updated dispute with resolution
    """
    dispute = DisputeManager.get_dispute(db, dispute_id)
    
    if not dispute:
        raise HTTPException(status_code=404, detail="Dispute not found")
    
    if resolution.resolution not in ["settlement_upheld", "settlement_reversed"]:
        raise HTTPException(
            status_code=400,
            detail="Resolution must be 'settlement_upheld' or 'settlement_reversed'"
        )
    
    # Resolve dispute
    resolved = DisputeManager.resolve_dispute(
        db=db,
        dispute_id=dispute_id,
        resolution=resolution.resolution,
        ruling=resolution.ruling,
        notes=resolution.notes
    )
    
    logger.info(f"Dispute resolved: {dispute_id} - {resolution.resolution}")
    
    return {
        "dispute_id": dispute_id,
        "resolution": resolution.resolution,
        "ruling": resolution.ruling,
        "resolved_at": resolved["resolved_at"],
        "status": resolved["status"],
        "message": "Dispute resolved successfully"
    }


@router.post("/{dispute_id}/appeal", response_model=dict, status_code=status.HTTP_201_CREATED)
async def appeal_dispute(
    dispute_id: str,
    appeal: DisputeAppeal,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user)
):
    """
    Appeal a dispute resolution.
    
    Allows parties to appeal a resolved dispute to a higher authority.
    
    Args:
        dispute_id: Dispute ID
        appeal: Appeal details
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Appeal record
    """
    dispute = DisputeManager.get_dispute(db, dispute_id)
    
    if not dispute:
        raise HTTPException(status_code=404, detail="Dispute not found")
    
    # Create appeal
    appeal_record = DisputeManager.appeal_dispute(
        db=db,
        dispute_id=dispute_id,
        appellant_id=current_user.id,
        appeal_reason=appeal.appeal_reason
    )
    
    logger.info(f"Dispute appealed: {appeal_record['appeal_id']} for dispute {dispute_id}")
    
    return {
        "appeal_id": appeal_record["appeal_id"],
        "dispute_id": dispute_id,
        "appeal_reason": appeal.appeal_reason,
        "created_at": appeal_record["created_at"],
        "status": appeal_record["status"],
        "message": "Appeal submitted successfully"
    }


@router.get("/agent/{agent_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def get_agent_disputes(
    agent_id: str,
    status_filter: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user)
):
    """
    Get disputes involving a specific agent.
    
    Args:
        agent_id: Agent ID
        status_filter: Optional status filter
        limit: Max disputes to return
        offset: Pagination offset
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of disputes for the agent
    """
    # Verify agent exists
    agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    disputes = DisputeManager.get_disputes_by_agent(
        db, agent_id, status_filter, limit, offset
    )
    
    return {
        "agent_id": agent_id,
        "disputes": disputes,
        "total_disputes": len(disputes),
        "limit": limit,
        "offset": offset,
        "filters": {"status": status_filter}
    }
