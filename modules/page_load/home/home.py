from fastapi import APIRouter, HTTPException, Header
from typing import Optional, Dict, Any, List
import aiohttp
import os
import json
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/page_load", tags=["page_load"])

async def get_user_from_token(authorization: Optional[str] = Header(None)) -> Optional[Dict[str, Any]]:
    """
    Extract user information from authorization token
    """
    if not authorization or not authorization.startswith("Bearer "):
        return None
    
    try:
        token = authorization.replace("Bearer ", "")
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        if not supabase_url or not supabase_service_key:
            return None
        
        # Verify token and get user info
        url = f"{supabase_url}/auth/v1/user"
        headers = {
            "apikey": supabase_service_key,
            "Authorization": f"Bearer {token}"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    user_data = await response.json()
                    return user_data
                else:
                    return None
                    
    except Exception:
        return None

async def get_all_properties() -> List[Dict[str, Any]]:
    """
    Fetch all properties from MLS
    """
    try:
        mls_url = os.getenv("MLS_URL")
        mls_token = os.getenv("MLS_AUTHTOKEN")
        
        if not mls_url or not mls_token:
            raise HTTPException(status_code=500, detail="MLS configuration missing")
        
        url = f"{mls_url}/Property"
        params = {
            "$top": 50,
            "$select": "*"
        }
        
        headers = {
            "Authorization": f"Bearer {mls_token}",
            "Content-Type": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("value", [])
                else:
                    raise HTTPException(status_code=response.status, detail="MLS API error")
                    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_user_details(user_id: str) -> Dict[str, Any]:
    """
    Get user details from Supabase
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

@router.get("/home")
async def get_home_data(authorization: Optional[str] = Header(None)):
    """
    Get merged home page data - properties and user info if logged in
    """
    try:
        # Get properties
        properties = await get_all_properties()
        
        # Check if user is logged in
        user_data = await get_user_from_token(authorization)
        
        if user_data and user_data.get("id"):
            # User is logged in - get full user details
            user_details = await get_user_details(user_data["id"])
            
            return {
                "user": {
                    "id": user_details.get("id"),
                    "name": f"{user_details.get('first_name', '')} {user_details.get('last_name', '')}".strip(),
                    "email": user_details.get("email"),
                    "avatar": user_details.get("profile_pic") or "/placeholder-user.jpg"
                },
                "properties": properties,
                "userPreferences": {
                    "notifications": True,  # Default values - could be fetched from user preferences
                    "darkMode": False,
                    "favoritePropertyIds": []  # Could be fetched from user's favorites
                },
                "recentlyViewed": [],  # Could be fetched from user's recently viewed
                "favorites": [],  # Could be fetched from user's favorites
                "showingRequests": []  # Could be fetched from user's showing requests
            }
        else:
            # User is not logged in - return properties only
            return {
                "properties": properties,
                "user": None,
                "userPreferences": None,
                "recentlyViewed": [],
                "favorites": [],
                "showingRequests": []
            }
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 