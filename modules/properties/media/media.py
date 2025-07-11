from fastapi import APIRouter, HTTPException
import aiohttp
import os
import json
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/properties", tags=["properties"])

@router.get("/media/{resource_record_key}")
async def get_property_media(resource_record_key: str):
    """
    Get property media by resource record key
    """
    try:
        mls_url = os.getenv("MLS_URL")
        mls_token = os.getenv("MLS_AUTHTOKEN")
        
        if not mls_url or not mls_token:
            raise HTTPException(status_code=500, detail="MLS configuration missing")
        
        # Build URL with filter
        url = f"{mls_url}/Media"
        params = {
            "$filter": f"ResourceRecordKey eq '{resource_record_key}'",
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
                    media_items = data.get("value", [])
                    
                    if not media_items:
                        raise HTTPException(status_code=404, detail="Media not found")
                    
                    return {
                        "@odata.context": f"{mls_url}/$metadata#Media",
                        "value": media_items
                    }
                else:
                    raise HTTPException(status_code=response.status, detail="MLS API error")
                    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/media/mapping/{listing_key}")
async def get_property_media_by_mapping(listing_key: str):
    """
    Get property media using the resource record key mapping
    """
    try:
        mapping_str = os.getenv("RESOURCE_RECORD_KEY_MAPPING", "{}")
        mapping = json.loads(mapping_str)
        
        if listing_key not in mapping:
            raise HTTPException(status_code=404, detail="No mapping found for listing key")
        
        resource_record_key = mapping[listing_key]
        return await get_property_media(resource_record_key)
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid mapping configuration")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 