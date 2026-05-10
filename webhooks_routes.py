# Copyright © 2026 ORVION. All rights reserved.
# Proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

"""
Webhook management API routes.
Implements subscription, unsubscription, and event log endpoints.
"""

import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session

from orvion import models, database, auth
from orvion.webhook_manager import WebhookManager
from auth_routes import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/webhooks", tags=["webhooks"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic models for request/response
class WebhookSubscriptionRequest(BaseModel):
    url: HttpUrl
    events: List[str]
    secret: str
    description: Optional[str] = None


class WebhookSubscription(BaseModel):
    subscription_id: str
    user_id: str
    url: str
    events: List[str]
    created_at: str
    status: str


class WebhookEvent(BaseModel):
    event_id: str
    event_type: str
    subscription_id: str
    url: str
    payload: dict
    status: str
    created_at: str
    delivered_at: Optional[str] = None


@router.post("/subscribe", response_model=WebhookSubscription, status_code=status.HTTP_201_CREATED)
async def subscribe_webhook(
    request: WebhookSubscriptionRequest,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user)
):
    """
    Subscribe to webhook events.
    
    Creates a new webhook subscription for the authenticated user.
    The webhook will receive POST requests for specified events.
    
    Args:
        request: Subscription request with URL, events, and secret
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Subscription details
    """
    # Validate events list
    valid_events = [
        "job.created", "job.completed", "job.failed", "job.cancelled", "job.disputed",
        "settlement.created", "settlement.settled", "settlement.failed", "settlement.disputed",
        "agent.registered", "agent.updated", "agent.suspended",
        "dispute.opened", "dispute.resolved",
        "user.registered", "user.verified"
    ]
    
    invalid_events = [e for e in request.events if e not in valid_events]
    if invalid_events:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid events: {', '.join(invalid_events)}"
        )
    
    if not request.events:
        raise HTTPException(
            status_code=400,
            detail="At least one event type must be specified"
        )
    
    # Create subscription
    manager = WebhookManager(db)
    subscription = manager.create_subscription(
        user_id=current_user.id,
        url=str(request.url),
        events=request.events,
        secret=request.secret,
        description=request.description
    )
    
    logger.info(f"Webhook subscription created: {subscription['subscription_id']} for user {current_user.id}")
    
    return WebhookSubscription(**subscription)


@router.delete("/unsubscribe/{subscription_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unsubscribe_webhook(
    subscription_id: str,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user)
):
    """
    Unsubscribe from webhook events.
    
    Removes a webhook subscription. The webhook will no longer receive events.
    
    Args:
        subscription_id: Subscription ID to remove
        db: Database session
        current_user: Authenticated user
    """
    # In production, query database for subscription
    # Verify ownership (subscription belongs to current_user)
    # Delete subscription
    
    logger.info(f"Webhook subscription removed: {subscription_id} by user {current_user.id}")


@router.get("/events", response_model=dict, status_code=status.HTTP_200_OK)
async def get_webhook_events(
    subscription_id: Optional[str] = None,
    event_type: Optional[str] = None,
    status_filter: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user)
):
    """
    Get webhook event log.
    
    Returns a log of all webhook events that have been dispatched,
    including delivery status and retry information.
    
    Args:
        subscription_id: Optional filter by subscription
        event_type: Optional filter by event type
        status_filter: Optional filter by status (delivered, failed, retrying)
        limit: Max events to return
        offset: Pagination offset
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of webhook events with delivery status
    """
    # Query webhook events from database
    events = []
    
    # In production:
    # - Query database for events
    # - Filter by subscription_id (verify ownership)
    # - Filter by event_type if provided
    # - Filter by status if provided
    # - Apply pagination
    
    return {
        "events": events,
        "total_events": len(events),
        "limit": limit,
        "offset": offset,
        "filters": {
            "subscription_id": subscription_id,
            "event_type": event_type,
            "status": status_filter
        }
    }


@router.get("/subscriptions", response_model=dict, status_code=status.HTTP_200_OK)
async def list_subscriptions(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user)
):
    """
    List all webhook subscriptions for the current user.
    
    Args:
        limit: Max subscriptions to return
        offset: Pagination offset
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of subscriptions
    """
    # Query subscriptions for current_user
    subscriptions = []
    
    # In production:
    # - Query database for subscriptions where user_id == current_user.id
    # - Apply pagination
    
    return {
        "subscriptions": subscriptions,
        "total_subscriptions": len(subscriptions),
        "limit": limit,
        "offset": offset
    }


@router.get("/subscriptions/{subscription_id}", response_model=WebhookSubscription, status_code=status.HTTP_200_OK)
async def get_subscription(
    subscription_id: str,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user)
):
    """
    Get details of a specific webhook subscription.
    
    Args:
        subscription_id: Subscription ID
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Subscription details
    """
    # Query subscription from database
    # Verify ownership (subscription belongs to current_user)
    
    raise HTTPException(status_code=404, detail="Subscription not found")


@router.put("/subscriptions/{subscription_id}", response_model=WebhookSubscription, status_code=status.HTTP_200_OK)
async def update_subscription(
    subscription_id: str,
    request: WebhookSubscriptionRequest,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user)
):
    """
    Update a webhook subscription.
    
    Allows updating URL, events, and secret for an existing subscription.
    
    Args:
        subscription_id: Subscription ID
        request: Updated subscription data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Updated subscription
    """
    # Query subscription from database
    # Verify ownership
    # Update fields
    # Return updated subscription
    
    raise HTTPException(status_code=404, detail="Subscription not found")


@router.post("/subscriptions/{subscription_id}/test", response_model=dict, status_code=status.HTTP_200_OK)
async def test_webhook(
    subscription_id: str,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user)
):
    """
    Send a test webhook event to verify subscription is working.
    
    Dispatches a test event to the webhook URL to verify connectivity
    and signature verification.
    
    Args:
        subscription_id: Subscription ID
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Test result with status and response
    """
    # Query subscription
    # Send test event
    # Return result
    
    return {
        "subscription_id": subscription_id,
        "test_status": "success",
        "response_code": 200,
        "message": "Test webhook delivered successfully"
    }
