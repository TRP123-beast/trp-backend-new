from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.user_service import user_service
from app.core.dependencies import get_current_user

router = APIRouter(tags=["users"])

@router.post("/auth/signup", response_model=UserResponse)
async def signup(user_data: UserCreate):
    """Create a new user account"""
    try:
        return await user_service.create_user(user_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/auth/login", response_model=Token)
async def login(user_data: UserLogin):
    """Authenticate user and return JWT token"""
    try:
        return await user_service.authenticate_user(user_data)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/auth/refresh", response_model=Token)
async def refresh_token(refresh_token: str):
    """Refresh JWT token"""
    try:
        return await user_service.refresh_token(refresh_token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/me", response_model=dict)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    return current_user 