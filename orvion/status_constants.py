# Copyright © 2026 ORVION. All rights reserved.
# Proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

"""
Status constants for ORVION platform.
Ensures consistency across settlement_engine, dashboard, and all routes.
"""

from enum import Enum


class JobStatus(str, Enum):
    """Status values for Jobs."""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    DISPUTED = "disputed"


class SettlementStatus(str, Enum):
    """Status values for Settlements - standardized to 'settled' for confirmed liquidations."""
    PENDING = "pending"
    SETTLED = "settled"  # Previously "confirmed" - now standardized
    FAILED = "failed"
    DISPUTED = "disputed"


class UserStatus(str, Enum):
    """Status values for Users."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    VERIFIED = "verified"
    UNVERIFIED = "unverified"


class AgentStatus(str, Enum):
    """Status values for Agents."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    OFFLINE = "offline"


class DisputeStatus(str, Enum):
    """Status values for Disputes."""
    OPEN = "open"
    IN_REVIEW = "in_review"
    RESOLVED = "resolved"
    CLOSED = "closed"
    APPEALED = "appealed"


class WebhookStatus(str, Enum):
    """Status values for Webhooks."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    FAILED = "failed"
    RETRYING = "retrying"


class EventType(str, Enum):
    """Event types for webhook subscriptions."""
    JOB_CREATED = "job.created"
    JOB_COMPLETED = "job.completed"
    JOB_FAILED = "job.failed"
    JOB_CANCELLED = "job.cancelled"
    JOB_DISPUTED = "job.disputed"
    
    SETTLEMENT_CREATED = "settlement.created"
    SETTLEMENT_SETTLED = "settlement.settled"
    SETTLEMENT_FAILED = "settlement.failed"
    SETTLEMENT_DISPUTED = "settlement.disputed"
    
    AGENT_REGISTERED = "agent.registered"
    AGENT_UPDATED = "agent.updated"
    AGENT_SUSPENDED = "agent.suspended"
    
    DISPUTE_OPENED = "dispute.opened"
    DISPUTE_RESOLVED = "dispute.resolved"
    
    USER_REGISTERED = "user.registered"
    USER_VERIFIED = "user.verified"


# Mapping for backward compatibility (if needed)
LEGACY_STATUS_MAP = {
    "confirmed": SettlementStatus.SETTLED,
    "completed": JobStatus.COMPLETED,
}
