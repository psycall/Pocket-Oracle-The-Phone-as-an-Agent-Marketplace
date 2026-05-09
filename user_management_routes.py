from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from orvion import database, auth, schemas
from orvion.auth import get_user_by_id, update_user
from main import get_db # Import centralized get_db
from auth_routes import get_current_user # Import centralized get_current_user

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("/list", response_model=List[schemas.User])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user) # Require authentication
):
    """List all users with pagination (Admin only in production)"""
    # In a real application, this endpoint would require admin privileges
    users = db.query(auth.User).offset(skip).limit(limit).all()
    return [schemas.User.model_validate(u) for u in users]


@router.get("/{user_id}", response_model=schemas.User)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user) # Require authentication
):
    """Get user by ID"""
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this user's profile")

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return schemas.User.model_validate(user)


@router.get("/{user_id}/profile", response_model=schemas.UserProfile)
async def get_user_profile(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user) # Require authentication
):
    """Get detailed user profile"""
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this user's profile")

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return schemas.UserProfile(
        **schemas.User.model_validate(user).model_dump(),
        accountAge=(datetime.utcnow() - user.created_at).days,
        lastUpdated=user.updated_at
    )


@router.put("/{user_id}", response_model=schemas.User)
async def update_user_profile(
    user_id: str,
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user) # Require authentication
):
    """Update user profile"""
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this user's profile")
    
    update_data = user_update.model_dump(exclude_unset=True)
    updated_user = update_user(db, user_id, **update_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.User.model_validate(updated_user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user) # Require authentication
):
    """Delete user account"""
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this user's account")
    
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    
    return # No content for 204


@router.get("/{user_id}/statistics", response_model=schemas.UserStatistics)
async def get_user_statistics(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user) # Require authentication
):
    """Get user statistics"""
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this user's statistics")

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # This is a placeholder - in production, query actual data
    return schemas.UserStatistics(
        userId=user_id,
        totalSettlements=0,
        totalVolume="$0.00",
        averageSettlementTime="0s",
        successRate="0%",
        lastActivity=user.updated_at,
    )


@router.post("/{user_id}/verify", response_model=schemas.User)
async def verify_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user) # Require authentication
):
    """Verify user account"""
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to verify this user's account")
    
    updated_user = update_user(db, user_id, verified=True)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.User.model_validate(updated_user)


@router.get("/{user_id}/preferences", response_model=schemas.UserPreferences)
async def get_user_preferences(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user) # Require authentication
):
    """Get user preferences"""
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this user's preferences")

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # In production, retrieve preferences from database
    return schemas.UserPreferences(
        userId=user_id,
        theme="dark",
        notifications=True,
        emailUpdates=True,
        language="en",
    )


@router.put("/{user_id}/preferences", response_model=schemas.UserPreferences)
async def update_user_preferences(
    user_id: str,
    preferences_update: schemas.UserPreferencesUpdate,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_user) # Require authentication
):
    """Update user preferences"""
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this user's preferences")
    
    # In production, store preferences in database
    # For now, just return the updated preferences
    return schemas.UserPreferences(
        userId=user_id,
        theme=preferences_update.theme or "dark",
        notifications=preferences_update.notifications if preferences_update.notifications is not None else True,
        emailUpdates=preferences_update.emailUpdates if preferences_update.emailUpdates is not None else True,
        language=preferences_update.language or "en",
    )
