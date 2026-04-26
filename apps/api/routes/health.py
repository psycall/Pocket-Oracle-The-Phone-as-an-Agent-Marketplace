"""
Orvion — Health Routes
Public health check for load balancers and uptime monitors.
"""

from datetime import datetime, timezone

from fastapi import APIRouter

from core.config import settings
from models.schemas import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse, summary="Health check")
async def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        node=settings.NODE_ID,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
