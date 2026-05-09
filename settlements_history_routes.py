from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timedelta
from orvion import database, auth
from orvion.models import Settlement
from orvion.auth import get_user_by_id

router = APIRouter(prefix="/api/v1/settlements-history", tags=["settlements-history"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = None, db: Session = Depends(get_db)):
    """Get current authenticated user"""
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    payload = auth.verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


@router.get("/user/{user_id}")
async def get_user_settlements(
    user_id: str,
    skip: int = 0,
    limit: int = 50,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get user's settlement history with pagination and filtering"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Query settlements for user
    query = db.query(Settlement).filter(
        Settlement.user_id == user_id
    )
    
    if status_filter:
        query = query.filter(Settlement.status == status_filter)
    
    total = query.count()
    settlements = query.order_by(Settlement.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "userId": user_id,
        "settlements": [
            {
                "id": s.id,
                "agentId": s.agent_id,
                "jobId": s.job_id,
                "amount": str(s.amount),
                "toAddress": s.to_address,
                "status": s.status,
                "transactionHash": s.transaction_hash,
                "createdAt": s.created_at.isoformat(),
                "updatedAt": s.updated_at.isoformat(),
            }
            for s in settlements
        ],
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.get("/user/{user_id}/stats")
async def get_user_settlement_stats(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get user settlement statistics"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    settlements = db.query(Settlement).filter(
        Settlement.user_id == user_id
    ).all()
    
    total_settlements = len(settlements)
    completed = len([s for s in settlements if s.status == "completed"])
    pending = len([s for s in settlements if s.status == "pending"])
    failed = len([s for s in settlements if s.status == "failed"])
    
    total_volume = sum(float(s.amount) for s in settlements if s.status == "completed")
    
    return {
        "userId": user_id,
        "totalSettlements": total_settlements,
        "completed": completed,
        "pending": pending,
        "failed": failed,
        "totalVolume": f"${total_volume:.2f}",
        "averageAmount": f"${total_volume / completed if completed > 0 else 0:.2f}",
        "successRate": f"{(completed / total_settlements * 100) if total_settlements > 0 else 0:.1f}%",
    }


@router.get("/user/{user_id}/daily-stats")
async def get_user_daily_stats(
    user_id: str,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get user daily settlement statistics"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    settlements = db.query(Settlement).filter(
        Settlement.user_id == user_id,
        Settlement.created_at >= start_date
    ).all()
    
    # Group by day
    daily_data = {}
    for settlement in settlements:
        day = settlement.created_at.date().isoformat()
        if day not in daily_data:
            daily_data[day] = {"count": 0, "volume": 0.0}
        daily_data[day]["count"] += 1
        if settlement.status == "completed":
            daily_data[day]["volume"] += float(settlement.amount)
    
    return {
        "userId": user_id,
        "period": f"Last {days} days",
        "data": [
            {
                "date": date,
                "count": stats["count"],
                "volume": f"${stats['volume']:.2f}",
            }
            for date, stats in sorted(daily_data.items())
        ],
    }


@router.get("/network/stats")
async def get_network_settlement_stats(
    db: Session = Depends(get_db)
):
    """Get network-wide settlement statistics"""
    all_settlements = db.query(Settlement).all()
    
    total_settlements = len(all_settlements)
    completed = len([s for s in all_settlements if s.status == "completed"])
    pending = len([s for s in all_settlements if s.status == "pending"])
    failed = len([s for s in all_settlements if s.status == "failed"])
    
    total_volume = sum(float(s.amount) for s in all_settlements if s.status == "completed")
    
    # Calculate average settlement time
    completed_settlements = [s for s in all_settlements if s.status == "completed"]
    avg_time = 0
    if completed_settlements:
        times = [(s.updated_at - s.created_at).total_seconds() for s in completed_settlements]
        avg_time = sum(times) / len(times)
    
    return {
        "totalSettlements": total_settlements,
        "completed": completed,
        "pending": pending,
        "failed": failed,
        "totalVolume": f"${total_volume:.2f}",
        "averageAmount": f"${total_volume / completed if completed > 0 else 0:.2f}",
        "successRate": f"{(completed / total_settlements * 100) if total_settlements > 0 else 0:.1f}%",
        "averageSettlementTime": f"{avg_time:.1f}s",
    }


@router.get("/network/daily-stats")
async def get_network_daily_stats(
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get network daily settlement statistics"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    settlements = db.query(Settlement).filter(
        Settlement.created_at >= start_date
    ).all()
    
    # Group by day
    daily_data = {}
    for settlement in settlements:
        day = settlement.created_at.date().isoformat()
        if day not in daily_data:
            daily_data[day] = {"count": 0, "volume": 0.0, "completed": 0}
        daily_data[day]["count"] += 1
        if settlement.status == "completed":
            daily_data[day]["volume"] += float(settlement.amount)
            daily_data[day]["completed"] += 1
    
    return {
        "period": f"Last {days} days",
        "data": [
            {
                "date": date,
                "count": stats["count"],
                "completed": stats["completed"],
                "volume": f"${stats['volume']:.2f}",
            }
            for date, stats in sorted(daily_data.items())
        ],
    }


@router.get("/{settlement_id}/details")
async def get_settlement_details(
    settlement_id: str,
    db: Session = Depends(get_db)
):
    """Get detailed settlement information"""
    settlement = db.query(Settlement).filter(Settlement.id == settlement_id).first()
    
    if not settlement:
        raise HTTPException(status_code=404, detail="Settlement not found")
    
    return {
        "id": settlement.id,
        "agentId": settlement.agent_id,
        "jobId": settlement.job_id,
        "amount": str(settlement.amount),
        "toAddress": settlement.to_address,
        "status": settlement.status,
        "transactionHash": settlement.transaction_hash,
        "createdAt": settlement.created_at.isoformat(),
        "updatedAt": settlement.updated_at.isoformat(),
        "processingTime": f"{(settlement.updated_at - settlement.created_at).total_seconds():.1f}s",
    }
