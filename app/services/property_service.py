import aiohttp
from typing import Optional, Dict, Any, List
from app.core.config import settings
from app.schemas.property import PropertyQuery, PropertyResponse, PropertyDetail, MediaResponse

class PropertyService:
    def __init__(self):
        self.mls_url = settings.MLS_URL
        self.mls_token = settings.MLS_AUTHTOKEN
    
    async def search_properties(self, query: PropertyQuery) -> PropertyResponse:
        """Search for properties with filters"""
        if not self.mls_url or not self.mls_token:
            raise Exception("MLS configuration missing")
        
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
        url = f"{self.mls_url}/Property"
        params = {
            "$top": query.MLS_TOP_LIMIT,
            "$select": query.MLS_PROPERTY_FILTER_FIELDS or "*"
        }
        
        if filter_string:
            params["$filter"] = filter_string
        
        headers = {
            "Authorization": f"Bearer {self.mls_token}",
            "Content-Type": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return PropertyResponse(
                        **{"@odata.context": f"{self.mls_url}/$metadata#Property"},
                        value=data.get("value", [])
                    )
                else:
                    raise Exception(f"MLS API error: {response.status}")
    
    async def get_property(self, property_id: str) -> PropertyDetail:
        """Get specific property details"""
        if not self.mls_url or not self.mls_token:
            raise Exception("MLS configuration missing")
        
        url = f"{self.mls_url}/Property('{property_id}')"
        headers = {
            "Authorization": f"Bearer {self.mls_token}",
            "Content-Type": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return PropertyDetail(**data)
                else:
                    raise Exception(f"Property not found: {response.status}")
    
    async def get_property_media(self, property_id: str) -> MediaResponse:
        """Get property media/images"""
        if not self.mls_url or not self.mls_token:
            raise Exception("MLS configuration missing")
        
        # This would need to be implemented based on your MLS API structure
        # for retrieving media/images for a property
        url = f"{self.mls_url}/Property('{property_id}')/Media"
        headers = {
            "Authorization": f"Bearer {self.mls_token}",
            "Content-Type": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    media_urls = [item.get("MediaURL") for item in data.get("value", [])]
                    return MediaResponse(
                        property_id=property_id,
                        media_urls=media_urls
                    )
                else:
                    raise Exception(f"Media not found: {response.status}")

property_service = PropertyService() 