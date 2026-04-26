"""
Orvion — Node Routes
GET /node/status  → node info + metrics
GET /node/history → task history (paginated)
POST /node/token  → get JWT access token
"""

import time
from fastapi import APIRouter, Depends, HTTPException, status

from core.memory import memory
from core.security import create_access_token, get_current_user
from core.config import settings
from models.schemas import NodeStatus, TokenResponse, TokenRequest

router = APIRouter()
_started_at = time.time()


@router.post("/token", response_model=TokenResponse, summary="Get access token")
async def get_token(body: TokenRequest):
    """
    Exchange your API key for a JWT access token.
    Use the returned token in the Authorization: Bearer <token> header.
    """
    if body.api_key != settings.SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    token = create_access_token({"sub": "api_user", "node": settings.NODE_ID})
    from datetime import timedelta
    return TokenResponse(
        access_token=token,
        expires_in=settings.JWT_EXPIRE_MINUTES * 60,
    )


@router.get("/status", response_model=NodeStatus, summary="Node status + metrics")
async def node_status(_user: dict = Depends(get_current_user)):
    total = await memory.count()
    return NodeStatus(
        node_id=settings.NODE_ID,
        version="2.0.0",
        status="running",
        environment=settings.ENVIRONMENT,
        tasks_executed=total,
        uptime_seconds=round(time.time() - _started_at, 2),
    )


@router.get("/history", summary="Paginated task history")
async def history(
    limit: int = 20,
    offset: int = 0,
    _user: dict = Depends(get_current_user),
):
    tasks = await memory.get_history(limit=limit, offset=offset)
    total = await memory.count()
    return {
        "tasks": tasks,
        "total": total,
        "limit": limit,
        "offset": offset,
    }
