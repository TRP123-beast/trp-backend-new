from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/properties", tags=["properties"])

class PropertyQuery(BaseModel):
    MLS_PROPERTY_TYPE: Optional[str] = None
    MLS_RENTAL_APPLICATION: Optional[str] = None
    MLS_ORIGINATING_SYSTEM_NAME: Optional[str] = None
    MLS_TOP_LIMIT: Optional[int] = 50
    MLS_PROPERTY_FILTER_FIELDS: Optional[str] = None

@router.post("/search")
async def search_properties(query: PropertyQuery):
    """
    Search for properties with filters
    """
    try:
        mls_url = os.getenv("MLS_URL")
        mls_token = os.getenv("MLS_AUTHTOKEN")
        
        if not mls_url or not mls_token:
            raise HTTPException(status_code=500, detail="MLS configuration missing")
        
        # Build filter string
        filters = []
        if query.MLS_PROPERTY_TYPE:
            filters.append(f"MLS_PROPERTY_TYPE eq '{query.MLS_PROPERTY_TYPE}'")
        if query.MLS_RENTAL_APPLICATION:
            filters.append(f"MLS_RENTAL_APPLICATION eq '{query.MLS_RENTAL_APPLICATION}'")
        if query.MLS_ORIGINATING_SYSTEM_NAME:
            filters.append(f"MLS_ORIGINATING_SYSTEM_NAME eq '{query.MLS_ORIGINATING_SYSTEM_NAME}'")
        
        filter_string = " and ".join(filters) if filters else ""
        
        # Build URL with parameters
        url = f"{mls_url}/Property"
        params = {
            "$top": query.MLS_TOP_LIMIT,
            "$select": query.MLS_PROPERTY_FILTER_FIELDS or "*"
        }
        
        if filter_string:
            params["$filter"] = filter_string
        
        headers = {
            "Authorization": f"Bearer {mls_token}",
            "Content-Type": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "@odata.context": f"{mls_url}/$metadata#Property",
                        "value": data.get("value", [])
                    }
                else:
                    raise HTTPException(status_code=response.status, detail="MLS API error")
                    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 