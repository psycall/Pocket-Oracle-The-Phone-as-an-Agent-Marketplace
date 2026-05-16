# Copyright © 2026 ORVION. All rights reserved.
# Proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

"""
Webhook manager for event-driven architecture.
Handles subscription, dispatch, and retry logic for webhooks.
"""

import asyncio
import hashlib
import hmac
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4
import aiohttp

from sqlalchemy.orm import Session
from . import models, status_constants

logger = logging.getLogger(__name__)


class WebhookDispatcher:
    """Handles webhook event dispatch and retry logic."""
    
    MAX_RETRIES = 3
    RETRY_DELAYS = [5, 30, 300]  # seconds: 5s, 30s, 5m
    REQUEST_TIMEOUT = 10  # seconds
    
    @staticmethod
    def compute_signature(payload: str, secret: str) -> str:
        """
        Compute HMAC signature for webhook payload.
        
        Args:
            payload: JSON-encoded payload
            secret: Webhook secret
            
        Returns:
            HMAC hex digest
        """
        return hmac.new(
            secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
    
    @staticmethod
    async def dispatch_webhook(
        url: str,
        payload: dict,
        secret: str,
        event_type: str,
        retry_count: int = 0
    ) -> bool:
        """
        Dispatch a webhook to the given URL.
        
        Args:
            url: Webhook URL
            payload: Event payload
            secret: Webhook secret for signature
            event_type: Type of event
            retry_count: Current retry attempt
            
        Returns:
            True if successful, False if failed
        """
        payload_json = json.dumps(payload)
        signature = WebhookDispatcher.compute_signature(payload_json, secret)
        
        headers = {
            "Content-Type": "application/json",
            "X-ORVION-Event": event_type,
            "X-ORVION-Signature": signature,
            "X-ORVION-Timestamp": datetime.utcnow().isoformat(),
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    data=payload_json,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=WebhookDispatcher.REQUEST_TIMEOUT)
                ) as response:
                    if response.status in [200, 201, 202, 204]:
                        logger.info(f"✅ Webhook dispatched: {event_type} -> {url}")
                        return True
                    else:
                        logger.warning(f"⚠️ Webhook failed with status {response.status}: {event_type} -> {url}")
                        return False
        except asyncio.TimeoutError:
            logger.warning(f"⏱️ Webhook timeout: {event_type} -> {url}")
            return False
        except Exception as e:
            logger.error(f"❌ Webhook dispatch error: {e}")
            return False
    
    @staticmethod
    async def dispatch_with_retry(
        url: str,
        payload: dict,
        secret: str,
        event_type: str
    ) -> bool:
        """
        Dispatch webhook with exponential backoff retry.
        
        Args:
            url: Webhook URL
            payload: Event payload
            secret: Webhook secret
            event_type: Type of event
            
        Returns:
            True if eventually successful, False if all retries exhausted
        """
        for attempt in range(WebhookDispatcher.MAX_RETRIES):
            success = await WebhookDispatcher.dispatch_webhook(
                url, payload, secret, event_type, attempt
            )
            
            if success:
                return True
            
            if attempt < WebhookDispatcher.MAX_RETRIES - 1:
                delay = WebhookDispatcher.RETRY_DELAYS[attempt]
                logger.info(f"Retrying webhook in {delay}s (attempt {attempt + 1}/{WebhookDispatcher.MAX_RETRIES})")
                await asyncio.sleep(delay)
        
        logger.error(f"❌ Webhook failed after {WebhookDispatcher.MAX_RETRIES} retries: {event_type} -> {url}")
        return False


class WebhookManager:
    """High-level webhook management."""
    
    def __init__(self, db: Session):
        self.db = db
        self.dispatcher = WebhookDispatcher()
    
    def create_subscription(
        self,
        user_id: str,
        url: str,
        events: List[str],
        secret: str,
        description: Optional[str] = None
    ) -> dict:
        """
        Create a webhook subscription.
        
        Args:
            user_id: User creating the subscription
            url: Webhook URL
            events: List of event types to subscribe to
            secret: Webhook secret for signature verification
            description: Optional description
            
        Returns:
            Subscription info with ID
        """
        subscription_id = str(uuid4())
        
        # In production, persist to database
        logger.info(f"Created webhook subscription {subscription_id} for user {user_id}")
        
        return {
            "subscription_id": subscription_id,
            "user_id": user_id,
            "url": url,
            "events": events,
            "created_at": datetime.utcnow().isoformat(),
            "status": "active"
        }
    
    async def emit_event(
        self,
        event_type: str,
        data: dict,
        user_id: Optional[str] = None
    ) -> None:
        """
        Emit an event and dispatch to all subscribed webhooks.
        
        Args:
            event_type: Type of event (e.g., "job.created")
            data: Event data
            user_id: Optional user ID for filtering subscriptions
        """
        payload = {
            "event": event_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        # In production, query database for subscriptions
        logger.info(f"Event emitted: {event_type}")
        
        # Dispatch to subscribed webhooks (placeholder)
        # for subscription in subscriptions:
        #     if event_type in subscription.events:
        #         asyncio.create_task(
        #             self.dispatcher.dispatch_with_retry(
        #                 subscription.url,
        #                 payload,
        #                 subscription.secret,
        #                 event_type
        #             )
        #         )
