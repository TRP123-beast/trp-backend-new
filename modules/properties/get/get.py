from fastapi import APIRouter, HTTPException
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/properties", tags=["properties"])

@router.get("/get/{listing_key}")
async def get_property(listing_key: str):
    """
    Get a specific property by listing key
    """
    try:
        mls_url = os.getenv("MLS_URL")
        mls_token = os.getenv("MLS_AUTHTOKEN")
        
        if not mls_url or not mls_token:
            raise HTTPException(status_code=500, detail="MLS configuration missing")
        
        # Build URL with filter
        url = f"{mls_url}/Property"
        params = {
            "$filter": f"ListingKey eq '{listing_key}'",
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
                    properties = data.get("value", [])
                    
                    if not properties:
                        raise HTTPException(status_code=404, detail="Property not found")
                    
                    return properties[0]
                else:
                    raise HTTPException(status_code=response.status, detail="MLS API error")
                    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 