"""
Rate Limiting Middleware
Protege a API contra abuse e DDoS
"""

import logging
import time
from typing import Dict, Tuple
from collections import defaultdict
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class RateLimiter:
    """Simple in-memory rate limiter"""

    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = defaultdict(list)

    def is_allowed(self, client_id: str) -> bool:
        """Check if request is allowed"""
        now = time.time()
        minute_ago = now - 60

        # Clean old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id] if req_time > minute_ago
        ]

        # Check limit
        if len(self.requests[client_id]) >= self.requests_per_minute:
            return False

        # Add new request
        self.requests[client_id].append(now)
        return True

    def get_remaining(self, client_id: str) -> int:
        """Get remaining requests for client"""
        now = time.time()
        minute_ago = now - 60

        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id] if req_time > minute_ago
        ]

        return max(0, self.requests_per_minute - len(self.requests[client_id]))


# Global rate limiter
rate_limiter = RateLimiter(requests_per_minute=100)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """FastAPI middleware for rate limiting"""

    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"

        # Skip rate limiting for health checks
        if request.url.path == "/health":
            return await call_next(request)

        # Check rate limit
        if not rate_limiter.is_allowed(client_ip):
            logger.warning(f"Rate limit exceeded for {client_ip}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later.",
            )

        # Add rate limit headers
        response = await call_next(request)
        remaining = rate_limiter.get_remaining(client_ip)

        response.headers["X-RateLimit-Limit"] = str(rate_limiter.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(time.time()) + 60)

        return response


# Endpoint-specific rate limiters
endpoint_limiters = {
    "/api/v1/settlement/settlements": RateLimiter(requests_per_minute=30),
    "/api/v1/discovery/agents": RateLimiter(requests_per_minute=50),
    "/api/v1/auth/login": RateLimiter(requests_per_minute=10),
    "/api/v1/auth/wallet-login": RateLimiter(requests_per_minute=10),
}


def check_endpoint_rate_limit(endpoint: str, client_id: str) -> Tuple[bool, int]:
    """Check endpoint-specific rate limit"""
    if endpoint not in endpoint_limiters:
        return True, 0

    limiter = endpoint_limiters[endpoint]
    is_allowed = limiter.is_allowed(client_id)
    remaining = limiter.get_remaining(client_id)

    return is_allowed, remaining
