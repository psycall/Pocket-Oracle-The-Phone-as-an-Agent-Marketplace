"""
Orvion — Health Routes
Public health check for load balancers and uptime monitors.
"""

from datetime import datetime
from fastapi import APIRouter
from models.schemas import HealthResponse
from core.config import settings

router = APIRouter()


@router.get("/health", response_model=HealthResponse, summary="Health check")
async def health():
    return HealthResponse(
        status="ok",
        node=settings.NODE_ID,
        timestamp=datetime.utcnow().isoformat(),
    )
