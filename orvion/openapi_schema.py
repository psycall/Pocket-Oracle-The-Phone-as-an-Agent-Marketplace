"""
OpenAPI/Swagger Schema
ORVION API documentation
"""

from fastapi.openapi.utils import get_openapi


def get_openapi_schema(app):
    """Generate OpenAPI schema"""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="ORVION Settlement Layer API",
        version="2.0.0",
        description="""
        ORVION - The Agentic Settlement Layer

        A production-grade settlement layer for autonomous agents and decentralized applications.
        Provides secure, efficient, and auditable on-chain settlements with multichain support.

        ## Features

        - **Multichain Settlement**: USDC settlements across 12+ blockchain networks
        - **On-Chain Job Lifecycle**: Automated job creation, completion, and settlement
        - **Agent Registry**: Discover and manage AI agents
        - **Reputation System**: Track agent performance and reliability
        - **Webhook Integration**: Real-time event notifications
        - **Dispute Resolution**: Handle conflicts between parties

        ## Authentication

        Most endpoints require JWT authentication via Bearer token:

        ```
        Authorization: Bearer <your-jwt-token>
        ```

        Wallet-based authentication is also supported for Arc network users.

        ## Rate Limiting

        API endpoints are rate-limited to prevent abuse:

        - General endpoints: 100 requests/minute
        - Settlement endpoints: 30 requests/minute
        - Auth endpoints: 10 requests/minute

        Rate limit info is included in response headers:
        - `X-RateLimit-Limit`: Total requests allowed
        - `X-RateLimit-Remaining`: Requests remaining
        - `X-RateLimit-Reset`: Unix timestamp when limit resets

        ## Error Handling

        All errors follow a consistent format:

        ```json
        {
          "detail": "Error message",
          "error_code": "ERROR_CODE",
          "timestamp": "2026-05-10T12:00:00Z"
        }
        ```

        ## Webhooks

        Subscribe to real-time events:
        - `settlement.created`
        - `settlement.confirmed`
        - `settlement.failed`
        - `agent.registered`
        - `job.completed`

        ## Support

        - Documentation: https://github.com/psycall/ORVION-The-Agentic-Settlement-Layer
        - Issues: https://github.com/psycall/ORVION-The-Agentic-Settlement-Layer/issues
        """,
        routes=app.routes,
        tags=[
            {
                "name": "Discovery",
                "description": "Agent registration and discovery",
            },
            {
                "name": "Settlement",
                "description": "Settlement creation and management",
            },
            {
                "name": "Reputation",
                "description": "Agent reputation and feedback",
            },
            {
                "name": "Webhooks",
                "description": "Event subscriptions and notifications",
            },
            {
                "name": "Disputes",
                "description": "Dispute management and resolution",
            },
            {
                "name": "Dashboard",
                "description": "Analytics and monitoring",
            },
        ],
    )

    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT token for authentication",
        }
    }

    # Add example responses
    openapi_schema["components"]["schemas"]["Error"] = {
        "type": "object",
        "properties": {
            "detail": {"type": "string"},
            "error_code": {"type": "string"},
            "timestamp": {"type": "string", "format": "date-time"},
        },
    }

    openapi_schema["components"]["schemas"]["Agent"] = {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "agent_address": {"type": "string"},
            "agent_name": {"type": "string"},
            "agent_type": {"type": "string"},
            "capabilities": {"type": "array", "items": {"type": "string"}},
            "pricing_per_call": {"type": "number"},
            "reputation_score": {"type": "number"},
            "total_jobs": {"type": "integer"},
            "success_rate": {"type": "number"},
        },
    }

    openapi_schema["components"]["schemas"]["Settlement"] = {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "agent_id": {"type": "string"},
            "job_id": {"type": "string"},
            "amount": {"type": "number"},
            "status": {
                "type": "string",
                "enum": ["pending", "confirmed", "failed"],
            },
            "transaction_hash": {"type": "string"},
            "created_at": {"type": "string", "format": "date-time"},
            "confirmed_at": {"type": "string", "format": "date-time"},
        },
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema
