import aiohttp
from typing import Optional, Dict, Any, List
from core.config import settings
from schemas.property import MLSAPIResponse, MLSPropertyDetails, PropertySearchParams, PropertyResponse, PropertyDetail, MediaResponse

class MLSAPIError(Exception):
    """Custom exception for MLS API errors."""
    def __init__(self, message: str, status_code: int = 500, detail: Any = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.detail = detail

class PropertyService:
    def __init__(self):
        self.mls_url = settings.MLS_URL
        self.mls_token = settings.MLS_AUTHTOKEN
    
    async def search_properties_mls(self) -> MLSAPIResponse:
        """Search for properties using MLS API with environment variables"""
        if not self.mls_url or not self.mls_token:
            raise MLSAPIError("MLS configuration missing", 500)
        
        # Build the OData filter query using environment variables
        filter_query = (
            f"PropertyType eq '{settings.MLS_PROPERTY_TYPE}' "
            f"and RentalApplicationYN eq {settings.MLS_RENTAL_APPLICATION} "
            f"and OriginatingSystemName eq '{settings.MLS_ORIFINATING_SYSTEM_NAME}'"
        )
        
        # Construct query parameters
        query_params = {
            "$filter": filter_query,
            "$top": settings.MLS_TOP_LIMIT,
            "$select": settings.MLS_PPROPERTY_FILTER_FIELDS
        }
        
        headers = {
            "Authorization": f"Bearer {self.mls_token}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.mls_url}/Property"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=query_params, headers=headers, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Validate response with Pydantic
                        validated_response = MLSAPIResponse(**data)
                        return validated_response
                    else:
                        error_text = await response.text()
                        raise MLSAPIError(
                            f"MLS API error: {response.status}",
                            response.status,
                            error_text
                        )
            except aiohttp.ClientError as e:
                raise MLSAPIError(f"Network error connecting to MLS API: {e}", 503)
            except Exception as e:
                raise MLSAPIError(f"Unexpected error: {e}", 500)
    
    async def search_properties(self, params: PropertySearchParams) -> PropertyResponse:
        """Legacy search method - keeping for compatibility"""
        if not self.mls_url or not self.mls_token:
            raise Exception("MLS configuration missing")
        
        filters = []
        if params.MLS_PROPERTY_TYPE:
            filters.append(f"PropertyType eq '{params.MLS_PROPERTY_TYPE}'")
        if params.MLS_RENTAL_APPLICATION is not None:
            filters.append(f"RentalApplicationYN eq {str(params.MLS_RENTAL_APPLICATION).lower()}")
        if params.MLS_ORIFINATING_SYSTEM_NAME:
            filters.append(f"OriginatingSystemName eq '{params.MLS_ORIFINATING_SYSTEM_NAME}'")
        filter_string = " and ".join(filters) if filters else None
        
        odata_params = {
            "$top": params.MLS_TOP_LIMIT,
            "$select": params.MLS_PPROPERTY_FILTER_FIELDS or "*"
        }
        if filter_string:
            odata_params["$filter"] = filter_string
        
        headers = {
            "Authorization": f"Bearer {self.mls_token}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.mls_url}/Property"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=odata_params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return PropertyResponse(
                        odata_context=data.get("@odata.context", ""),
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