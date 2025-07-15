import aiohttp
from typing import Optional, Dict, Any
from core.config import settings
from core.security import get_password_hash, verify_password, create_access_token
from schemas.user import UserCreate, UserLogin, UserResponse, Token

class UserService:
    def __init__(self):
        self.supabase_url = settings.SUPABASE_URL
        self.supabase_key = settings.SUPABASE_ANON_KEY
    
    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """Create a new user in Supabase"""
        if not self.supabase_url or not self.supabase_key:
            raise Exception("Supabase configuration missing")
        
        hashed_password = get_password_hash(user_data.password)
        
        async with aiohttp.ClientSession() as session:
            url = f"{self.supabase_url}/auth/v1/signup"
            headers = {
                "apikey": self.supabase_key,
                "Content-Type": "application/json"
            }
            payload = {
                "email": user_data.email,
                "password": user_data.password
            }
            
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return UserResponse(
                        id=data["user"]["id"],
                        email=data["user"]["email"],
                        created_at=data["user"]["created_at"]
                    )
                else:
                    error_data = await response.json()
                    raise Exception(f"User creation failed: {error_data}")
    
    async def authenticate_user(self, user_data: UserLogin) -> Token:
        """Authenticate user and return JWT token"""
        if not self.supabase_url or not self.supabase_key:
            raise Exception("Supabase configuration missing")
        
        async with aiohttp.ClientSession() as session:
            url = f"{self.supabase_url}/auth/v1/token?grant_type=password"
            headers = {
                "apikey": self.supabase_key,
                "Content-Type": "application/json"
            }
            payload = {
                "email": user_data.email,
                "password": user_data.password
            }
            
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return Token(access_token=data["access_token"])
                else:
                    error_data = await response.json()
                    raise Exception(f"Authentication failed: {error_data}")
    
    async def refresh_token(self, refresh_token: str) -> Token:
        """Refresh JWT token"""
        if not self.supabase_url or not self.supabase_key:
            raise Exception("Supabase configuration missing")
        
        async with aiohttp.ClientSession() as session:
            url = f"{self.supabase_url}/auth/v1/token?grant_type=refresh_token"
            headers = {
                "apikey": self.supabase_key,
                "Content-Type": "application/json"
            }
            payload = {
                "refresh_token": refresh_token
            }
            
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return Token(access_token=data["access_token"])
                else:
                    error_data = await response.json()
                    raise Exception(f"Token refresh failed: {error_data}")

user_service = UserService() 