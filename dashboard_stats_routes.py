from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from orvion import database, auth
from orvion.models import Agent, Settlement
from orvion.database import get_db # Import centralized get_db
from auth_routes import get_current_user # Import centralized get_current_user

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])


@router.get("/stats")
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user) # Ensure user is authenticated
):
    """Get comprehensive dashboard statistics"""
    
    # Get all agents
    all_agents = db.query(Agent).all()
    active_agents = len([a for a in all_agents if a.is_active])
    
    # Get all settlements
    all_settlements = db.query(Settlement).all()
    completed_settlements = [s for s in all_settlements if s.status == "completed"]
    pending_settlements = [s for s in all_settlements if s.status == "pending"]
    
    # Calculate volumes
    total_volume = sum(float(s.amount) for s in completed_settlements)
    volume_24h = sum(
        float(s.amount) for s in completed_settlements
        if (datetime.utcnow() - s.created_at).days < 1
    )
    
    # Calculate average settlement time
    avg_settlement_time = 0
    if completed_settlements:
        times = [(s.updated_at - s.created_at).total_seconds() for s in completed_settlements]
        avg_settlement_time = sum(times) / len(times)
    
    # Success rate
    total_count = len(all_settlements)
    success_rate = (len(completed_settlements) / total_count * 100) if total_count > 0 else 0
    
    return {
        "totalSettlements": len(all_settlements),
        "activeAgents": active_agents,
        "volume24h": f"${volume_24h:.2f}",
        "totalVolume": f"${total_volume:.2f}",
        "averageSettlementTime": f"{avg_settlement_time:.1f}s",
        "successRate": f"{success_rate:.1f}%",
        "pendingSettlements": len(pending_settlements),
        "completedSettlements": len(completed_settlements),
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/agents-overview")
async def get_agents_overview(
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user) # Ensure user is authenticated
):
    """Get agents overview for dashboard"""
    agents = db.query(Agent).limit(10).all()
    
    return {
        "agents": [
            {
                "id": a.id,
                "name": a.agent_name,
                "type": a.agent_type,
                "reputation": a.reputation,
                "earnings": f"${a.earnings:.2f}",
                "isActive": a.is_active,
            }
            for a in agents
        ],
        "total": db.query(Agent).count(),
    }


@router.get("/top-agents")
async def get_top_agents(
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user) # Ensure user is authenticated
):
    """Get top agents by reputation"""
    top_agents = db.query(Agent).order_by(
        Agent.reputation.desc()
    ).limit(limit).all()
    
    return {
        "topAgents": [
            {
                "id": a.id,
                "name": a.agent_name,
                "type": a.agent_type,
                "reputation": a.reputation,
                "earnings": f"${a.earnings:.2f}",
            }
            for a in top_agents
        ],
    }


@router.get("/settlement-trends")
async def get_settlement_trends(
    days: int = 7,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user) # Ensure user is authenticated
):
    """Get settlement trends over time"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    settlements = db.query(Settlement).filter(
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
        "period": f"Last {days} days",
        "trends": [
            {
                "date": date,
                "settlements": stats["count"],
                "volume": f"${stats['volume']:.2f}",
            }
            for date, stats in sorted(daily_data.items())
        ],
    }


@router.get("/network-health")
async def get_network_health(
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user) # Ensure user is authenticated
):
    """Get network health metrics"""
    all_agents = db.query(Agent).all()
    all_settlements = db.query(Settlement).all()
    
    active_agents = len([a for a in all_agents if a.is_active])
    avg_reputation = sum(a.reputation for a in all_agents) / len(all_agents) if all_agents else 0
    
    completed = len([s for s in all_settlements if s.status == "completed"])
    failed = len([s for s in all_settlements if s.status == "failed"])
    
    health_score = (completed / (completed + failed) * 100) if (completed + failed) > 0 else 0
    
    return {
        "healthScore": f"{health_score:.1f}%",
        "activeAgents": active_agents,
        "totalAgents": len(all_agents),
        "averageReputation": f"{avg_reputation:.1f}",
        "completedSettlements": completed,
        "failedSettlements": failed,
        "status": "Healthy" if health_score >= 90 else "Degraded" if health_score >= 70 else "Critical",
    }


@router.get("/recent-activity")
async def get_recent_activity(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user) # Ensure user is authenticated
):
    """Get recent settlement activity"""
    recent_settlements = db.query(Settlement).order_by(
        Settlement.created_at.desc()
    ).limit(limit).all()
    
    return {
        "recentActivity": [
            {
                "id": s.id,
                "agentId": s.agent_id,
                "jobId": s.job_id,
                "amount": str(s.amount),
                "status": s.status,
                "timestamp": s.created_at.isoformat(),
            }
            for s in recent_settlements
        ],
    }


@router.get("/metrics")
async def get_dashboard_metrics(
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user) # Ensure user is authenticated
):
    """Get all dashboard metrics in one call"""
    stats = await get_dashboard_stats(db, current_user)
    health = await get_network_health(db, current_user)
    agents = await get_agents_overview(db, current_user)
    activity = await get_recent_activity(db=db, current_user=current_user)
    
    return {
        "stats": stats,
        "health": health,
        "agents": agents,
        "recentActivity": activity,
        "generatedAt": datetime.utcnow().isoformat(),
    }
