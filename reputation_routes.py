# Copyright © 2026 ORVION. All rights reserved.
# Proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

"""
Agent reputation and trust API routes.
Implements reputation history, feedback, and top-rated agents endpoints.
"""

import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from orvion import models, database, auth
from orvion.reputation_engine import (
    ReputationCalculator,
    ReputationHistoryManager,
    FeedbackManager
)
from auth_routes import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/agents", tags=["reputation"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic models
class ReputationEvent(BaseModel):
    event_id: str
    agent_id: str
    old_score: float
    new_score: float
    change: float
    reason: str
    timestamp: str


class FeedbackSubmission(BaseModel):
    score: float = Field(..., ge=0, le=5)
    comment: Optional[str] = None
    settlement_id: Optional[str] = None


class AgentFeedback(BaseModel):
    feedback_id: str
    agent_id: str
    user_id: str
    score: float
    comment: Optional[str]
    settlement_id: Optional[str]
    created_at: str


class TopRatedAgent(BaseModel):
    agent_id: str
    agent_name: str
    agent_type: str
    reputation_score: float
    feedback_count: int
    average_feedback: float
    success_rate: float
    total_settlements: int


@router.get("/{agent_id}/reputation-history", response_model=dict, status_code=status.HTTP_200_OK)
async def get_reputation_history(
    agent_id: str,
    days: Optional[int] = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user)
):
    """
    Get reputation history for an agent.
    
    Returns a detailed timeline of reputation changes with events that caused them.
    
    Args:
        agent_id: Agent ID
        days: Optional filter for last N days
        limit: Max events to return
        offset: Pagination offset
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of reputation change events
    """
    # Verify agent exists
    agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Get reputation history
    history = ReputationHistoryManager.get_reputation_history(
        db, agent_id, limit, offset
    )
    
    # Calculate current reputation
    current_reputation = ReputationCalculator.calculate_overall_reputation(db, agent_id, days)
    
    return {
        "agent_id": agent_id,
        "agent_name": agent.agent_name,
        "current_reputation": current_reputation,
        "history": history,
        "total_events": len(history),
        "limit": limit,
        "offset": offset,
        "filters": {"days": days}
    }


@router.post("/{agent_id}/feedback", response_model=dict, status_code=status.HTTP_201_CREATED)
async def submit_feedback(
    agent_id: str,
    feedback: FeedbackSubmission,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user)
):
    """
    Submit feedback about an agent.
    
    Users can rate agents on a scale of 0-5 and provide comments.
    Feedback is used to calculate reputation scores.
    
    Args:
        agent_id: Agent ID
        feedback: Feedback data (score 0-5, optional comment)
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Feedback record
    """
    # Verify agent exists
    agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Submit feedback
    feedback_record = FeedbackManager.submit_feedback(
        db=db,
        agent_id=agent_id,
        user_id=current_user.id,
        score=feedback.score,
        comment=feedback.comment,
        settlement_id=feedback.settlement_id
    )
    
    logger.info(f"Feedback submitted: {agent_id} scored {feedback.score}/5 by {current_user.id}")
    
    return {
        "feedback_id": feedback_record["feedback_id"],
        "agent_id": agent_id,
        "score": feedback.score,
        "comment": feedback.comment,
        "created_at": feedback_record["created_at"],
        "message": "Feedback submitted successfully"
    }


@router.get("/{agent_id}/feedback", response_model=dict, status_code=status.HTTP_200_OK)
async def get_agent_feedback(
    agent_id: str,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user)
):
    """
    Get feedback for an agent.
    
    Returns all feedback submitted by users about the agent.
    
    Args:
        agent_id: Agent ID
        limit: Max feedback to return
        offset: Pagination offset
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of feedback records
    """
    # Verify agent exists
    agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Get feedback
    feedback_list = FeedbackManager.get_agent_feedback(db, agent_id, limit, offset)
    
    # Calculate statistics
    if feedback_list:
        average_score = sum(f["score"] for f in feedback_list) / len(feedback_list)
    else:
        average_score = 0.0
    
    return {
        "agent_id": agent_id,
        "agent_name": agent.agent_name,
        "feedback": feedback_list,
        "total_feedback": len(feedback_list),
        "average_score": average_score,
        "limit": limit,
        "offset": offset
    }


@router.get("/top-rated", response_model=dict, status_code=status.HTTP_200_OK)
async def get_top_rated_agents(
    agent_type: Optional[str] = None,
    min_reputation: float = 0.0,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user)
):
    """
    Get top-rated agents.
    
    Returns a list of agents with the highest reputation scores,
    optionally filtered by agent type or minimum reputation.
    
    Args:
        agent_type: Optional filter by agent type
        min_reputation: Minimum reputation score (0-100)
        limit: Max agents to return
        offset: Pagination offset
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of top-rated agents
    """
    # Get top-rated agents
    top_agents = FeedbackManager.get_top_rated_agents(
        db, limit, agent_type, min_reputation
    )
    
    return {
        "agents": top_agents,
        "total_agents": len(top_agents),
        "limit": limit,
        "offset": offset,
        "filters": {
            "agent_type": agent_type,
            "min_reputation": min_reputation
        }
    }


@router.get("/{agent_id}/reputation-score", response_model=dict, status_code=status.HTTP_200_OK)
async def get_agent_reputation_score(
    agent_id: str,
    days: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user)
):
    """
    Get current reputation score for an agent.
    
    Calculates the overall reputation score based on performance metrics.
    
    Args:
        agent_id: Agent ID
        days: Optional time window (None = all time)
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Reputation score and breakdown
    """
    # Verify agent exists
    agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Calculate reputation components
    success_rate = ReputationCalculator.calculate_success_rate(db, agent_id, days)
    response_time = ReputationCalculator.calculate_average_response_time(db, agent_id, days)
    settlement_time = ReputationCalculator.calculate_average_settlement_time(db, agent_id, days)
    feedback_score = ReputationCalculator.calculate_feedback_score(db, agent_id, days)
    overall_score = ReputationCalculator.calculate_overall_reputation(db, agent_id, days)
    
    return {
        "agent_id": agent_id,
        "agent_name": agent.agent_name,
        "overall_reputation": overall_score,
        "breakdown": {
            "success_rate": success_rate,
            "average_response_time_seconds": response_time,
            "average_settlement_time_minutes": settlement_time,
            "average_feedback_score": feedback_score
        },
        "time_window_days": days,
        "last_updated": None  # Would be actual timestamp
    }
