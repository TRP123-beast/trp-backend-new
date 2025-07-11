from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional, Dict, Any
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/users/auth", tags=["users"])

class SignupRequest(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    role: str = "user"

class LoginRequest(BaseModel):
    email: str
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

class CreateUserRequest(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    role: str = "user"
    phone: Optional[str] = None
    profile_pic: Optional[str] = None
    lsp_count: int = 0

class UpdateUserRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    phone: Optional[str] = None
    profile_pic: Optional[str] = None
    lsp_count: Optional[int] = None

@router.post("/signup")
async def signup(request: SignupRequest):
    """
    User signup endpoint
    """
    try:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_anon_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_anon_key:
            raise HTTPException(status_code=500, detail="Supabase configuration missing")
        
        url = f"{supabase_url}/auth/v1/signup"
        headers = {
            "apikey": supabase_anon_key,
            "Content-Type": "application/json"
        }
        
        body = {
            "email": request.email,
            "password": request.password,
            "data": {
                "first_name": request.first_name,
                "last_name": request.last_name,
                "role": request.role
            }
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=body, headers=headers) as response:
                data = await response.json()
                
                if response.status == 200:
                    return data
                else:
                    raise HTTPException(status_code=response.status, detail=data.get("error_description", "Signup failed"))
                    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/token")
async def login(request: LoginRequest):
    """
    User login endpoint
    """
    try:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_anon_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_anon_key:
            raise HTTPException(status_code=500, detail="Supabase configuration missing")
        
        url = f"{supabase_url}/auth/v1/token?grant_type=password"
        headers = {
            "apikey": supabase_anon_key,
            "Content-Type": "application/json"
        }
        
        body = {
            "email": request.email,
            "password": request.password
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=body, headers=headers) as response:
                data = await response.json()
                
                if response.status == 200:
                    return data
                else:
                    raise HTTPException(status_code=response.status, detail=data.get("error_description", "Login failed"))
                    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/refresh")
async def refresh_token(request: RefreshRequest):
    """
    Refresh access token endpoint
    """
    try:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_anon_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_anon_key:
            raise HTTPException(status_code=500, detail="Supabase configuration missing")
        
        url = f"{supabase_url}/auth/v1/token?grant_type=refresh_token"
        headers = {
            "apikey": supabase_anon_key,
            "Content-Type": "application/json"
        }
        
        body = {
            "refresh_token": request.refresh_token
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=body, headers=headers) as response:
                data = await response.json()
                
                if response.status == 200:
                    return data
                else:
                    raise HTTPException(status_code=response.status, detail=data.get("error_description", "Token refresh failed"))
                    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create")
async def create_user(request: CreateUserRequest):
    """
    Create user in database (requires service role key)
    """
    try:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        if not supabase_url or not supabase_service_key:
            raise HTTPException(status_code=500, detail="Supabase configuration missing")
        
        url = f"{supabase_url}/rest/v1/users"
        headers = {
            "apikey": supabase_service_key,
            "Authorization": f"Bearer {supabase_service_key}",
            "Content-Type": "application/json"
        }
        
        body = {
            "id": request.id,
            "first_name": request.first_name,
            "last_name": request.last_name,
            "email": request.email,
            "role": request.role,
            "phone": request.phone,
            "profile_pic": request.profile_pic,
            "lsp_count": request.lsp_count
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=body, headers=headers) as response:
                data = await response.json()
                
                if response.status == 201:
                    return data
                else:
                    raise HTTPException(status_code=response.status, detail="User creation failed")
                    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all")
async def get_all_users():
    """
    Get all users (requires service role key)
    """
    try:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        if not supabase_url or not supabase_service_key:
            raise HTTPException(status_code=500, detail="Supabase configuration missing")
        
        url = f"{supabase_url}/rest/v1/users?select=*"
        headers = {
            "apikey": supabase_service_key,
            "Authorization": f"Bearer {supabase_service_key}"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise HTTPException(status_code=response.status, detail="Failed to fetch users")
                    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}")
async def get_user(user_id: str):
    """
    Get specific user by ID
    """
    try:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        if not supabase_url or not supabase_service_key:
            raise HTTPException(status_code=500, detail="Supabase configuration missing")
        
        url = f"{supabase_url}/rest/v1/users?id=eq.{user_id}&select=*"
        headers = {
            "apikey": supabase_service_key,
            "Authorization": f"Bearer {supabase_service_key}"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    if not data:
                        raise HTTPException(status_code=404, detail="User not found")
                    return data[0]
                else:
                    raise HTTPException(status_code=response.status, detail="Failed to fetch user")
                    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{user_id}")
async def update_user(user_id: str, request: UpdateUserRequest):
    """
    Update user details
    """
    try:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        if not supabase_url or not supabase_service_key:
            raise HTTPException(status_code=500, detail="Supabase configuration missing")
        
        url = f"{supabase_url}/rest/v1/users?id=eq.{user_id}"
        headers = {
            "apikey": supabase_service_key,
            "Authorization": f"Bearer {supabase_service_key}",
            "Content-Type": "application/json"
        }
        
        # Only include non-None values
        body = {k: v for k, v in request.dict().items() if v is not None}
        
        async with aiohttp.ClientSession() as session:
            async with session.patch(url, json=body, headers=headers) as response:
                if response.status == 204:
                    return {"message": "User updated successfully"}
                else:
                    raise HTTPException(status_code=response.status, detail="Failed to update user")
                    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{user_id}")
async def delete_user(user_id: str):
    """
    Delete user
    """
    try:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        if not supabase_url or not supabase_service_key:
            raise HTTPException(status_code=500, detail="Supabase configuration missing")
        
        url = f"{supabase_url}/rest/v1/users?id=eq.{user_id}"
        headers = {
            "apikey": supabase_service_key,
            "Authorization": f"Bearer {supabase_service_key}"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=headers) as response:
                if response.status == 204:
                    return {"message": "User deleted successfully"}
                else:
                    raise HTTPException(status_code=response.status, detail="Failed to delete user")
                    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 