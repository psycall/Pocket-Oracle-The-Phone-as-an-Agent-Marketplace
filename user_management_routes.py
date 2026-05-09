from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from orvion import database, auth
from orvion.auth import get_user_by_id, user_to_dict, update_user

router = APIRouter(prefix="/api/v1/users", tags=["users"])


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


@router.get("/list")
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all users with pagination"""
    users = db.query(auth.User).offset(skip).limit(limit).all()
    total = db.query(auth.User).count()
    
    return {
        "users": [user_to_dict(u) for u in users],
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.get("/{user_id}")
async def get_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get user by ID"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user_to_dict(user)


@router.get("/{user_id}/profile")
async def get_user_profile(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get detailed user profile"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        **user_to_dict(user),
        "accountAge": (datetime.utcnow() - user.created_at).days,
        "lastUpdated": user.updated_at.isoformat(),
    }


@router.put("/{user_id}")
async def update_user_profile(
    user_id: str,
    name: Optional[str] = None,
    wallet_address: Optional[str] = None,
    token: str = None,
    db: Session = Depends(get_db)
):
    """Update user profile"""
    current_user = get_current_user(token, db)
    
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Cannot update other users")
    
    update_data = {}
    if name:
        update_data["name"] = name
    if wallet_address:
        update_data["wallet_address"] = wallet_address
    
    updated_user = update_user(db, user_id, **update_data)
    return user_to_dict(updated_user)


@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    token: str = None,
    db: Session = Depends(get_db)
):
    """Delete user account"""
    current_user = get_current_user(token, db)
    
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Cannot delete other users")
    
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully"}


@router.get("/{user_id}/statistics")
async def get_user_statistics(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get user statistics"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # This is a placeholder - in production, query actual data
    return {
        "userId": user_id,
        "totalSettlements": 0,
        "totalVolume": "$0.00",
        "averageSettlementTime": "0s",
        "successRate": "0%",
        "lastActivity": user.updated_at.isoformat(),
    }


@router.post("/{user_id}/verify")
async def verify_user(
    user_id: str,
    token: str = None,
    db: Session = Depends(get_db)
):
    """Verify user account"""
    current_user = get_current_user(token, db)
    
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Cannot verify other users")
    
    updated_user = update_user(db, user_id, verified=True)
    return user_to_dict(updated_user)


@router.get("/{user_id}/preferences")
async def get_user_preferences(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get user preferences"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "userId": user_id,
        "theme": "dark",
        "notifications": True,
        "emailUpdates": True,
        "language": "en",
    }


@router.put("/{user_id}/preferences")
async def update_user_preferences(
    user_id: str,
    theme: Optional[str] = None,
    notifications: Optional[bool] = None,
    emailUpdates: Optional[bool] = None,
    token: str = None,
    db: Session = Depends(get_db)
):
    """Update user preferences"""
    current_user = get_current_user(token, db)
    
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Cannot update other users preferences")
    
    # In production, store preferences in database
    return {
        "userId": user_id,
        "theme": theme or "dark",
        "notifications": notifications if notifications is not None else True,
        "emailUpdates": emailUpdates if emailUpdates is not None else True,
        "language": "en",
        "updated": True,
    }
