# Copyright © 2026 ORVION. All rights reserved.
# Proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

"""
Reputation engine for agent trust scoring and history tracking.
Implements reputation calculation, feedback collection, and historical analysis.
"""

import logging
from datetime import datetime, timedelta
from typing import List, Optional
from uuid import uuid4

from sqlalchemy.orm import Session
from . import models

logger = logging.getLogger(__name__)


class ReputationCalculator:
    """Calculates agent reputation scores based on historical performance."""
    
    # Weights for reputation calculation
    WEIGHT_SUCCESS_RATE = 0.40
    WEIGHT_RESPONSE_TIME = 0.25
    WEIGHT_SETTLEMENT_TIME = 0.20
    WEIGHT_FEEDBACK_SCORE = 0.15
    
    # Time windows for calculation
    WINDOW_RECENT_DAYS = 30
    WINDOW_ALL_TIME = None
    
    @staticmethod
    def calculate_success_rate(
        db: Session,
        agent_id: str,
        days: Optional[int] = WINDOW_RECENT_DAYS
    ) -> float:
        """
        Calculate agent's job completion success rate.
        
        Args:
            db: Database session
            agent_id: Agent ID
            days: Number of days to consider (None = all time)
            
        Returns:
            Success rate as percentage (0-100)
        """
        # Query completed jobs vs total jobs
        # Placeholder: return 95.0
        return 95.0
    
    @staticmethod
    def calculate_average_response_time(
        db: Session,
        agent_id: str,
        days: Optional[int] = WINDOW_RECENT_DAYS
    ) -> float:
        """
        Calculate average response time in seconds.
        
        Args:
            db: Database session
            agent_id: Agent ID
            days: Number of days to consider
            
        Returns:
            Average response time in seconds
        """
        # Query execution receipts and calculate time delta
        # Placeholder: return 2.5
        return 2.5
    
    @staticmethod
    def calculate_average_settlement_time(
        db: Session,
        agent_id: str,
        days: Optional[int] = WINDOW_RECENT_DAYS
    ) -> float:
        """
        Calculate average settlement time in minutes.
        
        Args:
            db: Database session
            agent_id: Agent ID
            days: Number of days to consider
            
        Returns:
            Average settlement time in minutes
        """
        # Query settlements and calculate time delta
        # Placeholder: return 15.0
        return 15.0
    
    @staticmethod
    def calculate_feedback_score(
        db: Session,
        agent_id: str,
        days: Optional[int] = WINDOW_RECENT_DAYS
    ) -> float:
        """
        Calculate average feedback score from users.
        
        Args:
            db: Database session
            agent_id: Agent ID
            days: Number of days to consider
            
        Returns:
            Average feedback score (0-5)
        """
        # Query feedback entries and calculate average
        # Placeholder: return 4.7
        return 4.7
    
    @classmethod
    def calculate_overall_reputation(
        cls,
        db: Session,
        agent_id: str,
        days: Optional[int] = WINDOW_RECENT_DAYS
    ) -> float:
        """
        Calculate overall reputation score using weighted formula.
        
        Args:
            db: Database session
            agent_id: Agent ID
            days: Number of days to consider
            
        Returns:
            Overall reputation score (0-100)
        """
        success_rate = cls.calculate_success_rate(db, agent_id, days)
        response_time = cls.calculate_average_response_time(db, agent_id, days)
        settlement_time = cls.calculate_average_settlement_time(db, agent_id, days)
        feedback_score = cls.calculate_feedback_score(db, agent_id, days)
        
        # Normalize metrics to 0-100 scale
        response_time_score = max(0, 100 - (response_time * 10))  # Penalize slow responses
        settlement_time_score = max(0, 100 - (settlement_time / 60 * 10))  # Penalize slow settlements
        feedback_score_normalized = (feedback_score / 5.0) * 100
        
        # Calculate weighted score
        overall_score = (
            (success_rate * cls.WEIGHT_SUCCESS_RATE) +
            (response_time_score * cls.WEIGHT_RESPONSE_TIME) +
            (settlement_time_score * cls.WEIGHT_SETTLEMENT_TIME) +
            (feedback_score_normalized * cls.WEIGHT_FEEDBACK_SCORE)
        )
        
        return min(100, max(0, overall_score))


class ReputationHistoryManager:
    """Manages reputation history and change tracking."""
    
    @staticmethod
    def record_reputation_change(
        db: Session,
        agent_id: str,
        old_score: float,
        new_score: float,
        reason: str,
        metadata: Optional[dict] = None
    ) -> dict:
        """
        Record a reputation change event.
        
        Args:
            db: Database session
            agent_id: Agent ID
            old_score: Previous reputation score
            new_score: New reputation score
            reason: Reason for change
            metadata: Additional metadata
            
        Returns:
            Event record
        """
        event_id = str(uuid4())
        change = new_score - old_score
        
        event = {
            "event_id": event_id,
            "agent_id": agent_id,
            "old_score": old_score,
            "new_score": new_score,
            "change": change,
            "reason": reason,
            "metadata": metadata or {},
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        logger.info(f"Reputation change recorded: {agent_id} ({old_score:.1f} -> {new_score:.1f})")
        
        return event
    
    @staticmethod
    def get_reputation_history(
        db: Session,
        agent_id: str,
        limit: int = 100,
        offset: int = 0
    ) -> List[dict]:
        """
        Get reputation change history for an agent.
        
        Args:
            db: Database session
            agent_id: Agent ID
            limit: Max records to return
            offset: Pagination offset
            
        Returns:
            List of reputation change events
        """
        # Query reputation events from database
        # Placeholder: return []
        return []


class FeedbackManager:
    """Manages user feedback about agents."""
    
    @staticmethod
    def submit_feedback(
        db: Session,
        agent_id: str,
        user_id: str,
        score: float,
        comment: Optional[str] = None,
        settlement_id: Optional[str] = None
    ) -> dict:
        """
        Submit feedback about an agent.
        
        Args:
            db: Database session
            agent_id: Agent ID
            user_id: User ID providing feedback
            score: Feedback score (0-5)
            comment: Optional comment
            settlement_id: Optional settlement ID this feedback relates to
            
        Returns:
            Feedback record
        """
        if not (0 <= score <= 5):
            raise ValueError("Feedback score must be between 0 and 5")
        
        feedback_id = str(uuid4())
        
        feedback = {
            "feedback_id": feedback_id,
            "agent_id": agent_id,
            "user_id": user_id,
            "score": score,
            "comment": comment,
            "settlement_id": settlement_id,
            "created_at": datetime.utcnow().isoformat(),
        }
        
        logger.info(f"Feedback submitted: {agent_id} scored {score}/5 by {user_id}")
        
        return feedback
    
    @staticmethod
    def get_agent_feedback(
        db: Session,
        agent_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[dict]:
        """
        Get feedback for an agent.
        
        Args:
            db: Database session
            agent_id: Agent ID
            limit: Max records to return
            offset: Pagination offset
            
        Returns:
            List of feedback records
        """
        # Query feedback from database
        # Placeholder: return []
        return []
    
    @staticmethod
    def get_top_rated_agents(
        db: Session,
        limit: int = 10,
        agent_type: Optional[str] = None,
        min_reputation: float = 0.0
    ) -> List[dict]:
        """
        Get top-rated agents.
        
        Args:
            db: Database session
            limit: Max agents to return
            agent_type: Optional filter by agent type
            min_reputation: Minimum reputation score
            
        Returns:
            List of top-rated agents with scores
        """
        # Query agents ordered by reputation
        # Placeholder: return []
        return []
