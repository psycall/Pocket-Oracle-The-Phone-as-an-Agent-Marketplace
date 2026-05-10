from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
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
    oauth2_scheme # Import the centralized OAuth2 scheme
)
from main import get_db # Import centralized get_db

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_token(token)
        if payload is None:
            raise credentials_exception
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    user = get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception
    return user


@router.post("/signup", response_model=schemas.Token)
async def signup(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """Sign up new user"""
    # Check if user already exists
    existing_user = get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    user = create_user(db, user_in.email, user_in.password, user_in.name, user_in.wallet_address)
    
    # Create tokens
    access_token = create_access_token({"sub": user.id})
    refresh_token = create_refresh_token({"sub": user.id})
    
    return {
        "accessToken": access_token,
        "refreshToken": refresh_token,
        "expiresIn": auth.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "token_type": "bearer"
    }


@router.post("/login", response_model=schemas.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login with email and password"""
    user = get_user_by_email(db, form_data.username)
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    # Create tokens
    access_token = create_access_token({"sub": user.id})
    refresh_token = create_refresh_token({"sub": user.id})
    
    return {
        "accessToken": access_token,
        "refreshToken": refresh_token,
        "expiresIn": auth.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "token_type": "bearer"
    }


@router.post("/wallet-login", response_model=schemas.Token)
async def wallet_login(
    wallet_address: str,
    signature: str,
    db: Session = Depends(get_db)
):
    """Login with wallet signature (Development Only - Signature not verified)"""
    # In production, verify the signature against the wallet address
    # For now, we'll create/get user by wallet
    
    user = auth.get_user_by_wallet(db, wallet_address)
    
    if not user:
        # Create new user from wallet
        from uuid import uuid4
        user = auth.create_user(
            db,
            email=f"{wallet_address}@wallet.local",
            password=str(uuid4()), # Generate a random password for wallet-created users
            name=f"User-{wallet_address[:6]}",
            wallet_address=wallet_address
        )
    
    # Create tokens
    access_token = create_access_token({"sub": user.id})
    refresh_token = create_refresh_token({"sub": user.id})
    
    return {
        "accessToken": access_token,
        "refreshToken": refresh_token,
        "expiresIn": auth.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=schemas.Token)
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
        "expiresIn": auth.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "token_type": "bearer"
    }


@router.get("/me", response_model=schemas.User)
async def get_me(
    current_user: auth.User = Depends(get_current_user)
):
    """Get current user profile"""
    return current_user


@router.put("/profile", response_model=schemas.User)
async def update_profile(
    user_update: schemas.UserUpdate,
    current_user: auth.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile"""
    update_data = user_update.model_dump(exclude_unset=True)
    updated_user = auth.update_user(db, current_user.id, **update_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.post("/logout")
async def logout(current_user: auth.User = Depends(get_current_user)):
    """Logout user"""
    # In production, you might want to blacklist the token
    return {"message": "Logged out successfully"}
