from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from orvion import auth, database, schemas
from orvion.auth import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
    user_to_dict,
)

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


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
    
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


@router.post("/signup")
async def signup(
    email: str,
    password: str,
    name: str,
    wallet_address: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Sign up new user"""
    # Check if user already exists
    existing_user = get_user_by_email(db, email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    user = create_user(db, email, password, name, wallet_address)
    
    # Create tokens
    access_token = create_access_token({"sub": user.id})
    refresh_token = create_refresh_token({"sub": user.id})
    
    return {
        "user": user_to_dict(user),
        "accessToken": access_token,
        "refreshToken": refresh_token,
        "expiresIn": 1800,
    }


@router.post("/login")
async def login(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    """Login with email and password"""
    user = get_user_by_email(db, email)
    
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create tokens
    access_token = create_access_token({"sub": user.id})
    refresh_token = create_refresh_token({"sub": user.id})
    
    return {
        "user": user_to_dict(user),
        "accessToken": access_token,
        "refreshToken": refresh_token,
        "expiresIn": 1800,
    }


@router.post("/wallet-login")
async def wallet_login(
    wallet_address: str,
    signature: str,
    db: Session = Depends(get_db)
):
    """Login with wallet signature"""
    # In production, verify the signature against the wallet address
    # For now, we'll create/get user by wallet
    
    user = auth.get_user_by_wallet(db, wallet_address)
    
    if not user:
        # Create new user from wallet
        from uuid import uuid4
        user = auth.create_user(
            db,
            email=f"{wallet_address}@wallet.local",
            password="",
            name=f"User-{wallet_address[:6]}",
            wallet_address=wallet_address
        )
    
    # Create tokens
    access_token = create_access_token({"sub": user.id})
    refresh_token = create_refresh_token({"sub": user.id})
    
    return {
        "user": user_to_dict(user),
        "accessToken": access_token,
        "refreshToken": refresh_token,
        "expiresIn": 1800,
    }


@router.post("/refresh")
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """Refresh access token"""
    payload = verify_token(refresh_token)
    
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    user_id = payload.get("sub")
    user = get_user_by_id(db, user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create new tokens
    access_token = create_access_token({"sub": user.id})
    new_refresh_token = create_refresh_token({"sub": user.id})
    
    return {
        "accessToken": access_token,
        "refreshToken": new_refresh_token,
        "expiresIn": 1800,
    }


@router.get("/me")
async def get_me(
    token: str = None,
    db: Session = Depends(get_db)
):
    """Get current user profile"""
    user = get_current_user(token, db)
    return user_to_dict(user)


@router.put("/profile")
async def update_profile(
    name: Optional[str] = None,
    wallet_address: Optional[str] = None,
    token: str = None,
    db: Session = Depends(get_db)
):
    """Update user profile"""
    user = get_current_user(token, db)
    
    update_data = {}
    if name:
        update_data["name"] = name
    if wallet_address:
        update_data["wallet_address"] = wallet_address
    
    updated_user = auth.update_user(db, user.id, **update_data)
    return user_to_dict(updated_user)


@router.post("/logout")
async def logout(token: str = None):
    """Logout user"""
    # In production, you might want to blacklist the token
    return {"message": "Logged out successfully"}
