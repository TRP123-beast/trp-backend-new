import aiohttp
from typing import Optional, Dict, Any, List
from core.config import settings
from schemas.property import MLSAPIResponse, MLSPropertyDetails, PropertySearchParams, PropertyResponse, PropertyDetail, MediaResponse
import logging

logger = logging.getLogger("mls_proxy")
logging.basicConfig(level=logging.INFO)

def strip_quotes(val):
    if isinstance(val, str) and val.startswith('"') and val.endswith('"'):
        return val[1:-1]
    return val

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
    
    async def search_properties_mls(self, property_type: Optional[str] = None, rental_application_yn: Optional[bool] = None, top_limit: Optional[int] = None, originating_system_name: Optional[str] = None) -> MLSAPIResponse:
        """Search for properties using MLS API with environment variables or dynamic params"""
        if not self.mls_url or not self.mls_token:
            raise MLSAPIError("MLS configuration missing", 500)
        
        # Use dynamic params if provided, else fallback to env
        property_type = strip_quotes(property_type or settings.MLS_PROPERTY_TYPE)
        originating_system_name = strip_quotes(originating_system_name or settings.MLS_ORIFINATING_SYSTEM_NAME)
        rental_application_yn = (
            rental_application_yn if rental_application_yn is not None
            else (settings.MLS_RENTAL_APPLICATION.lower() == "true" if isinstance(settings.MLS_RENTAL_APPLICATION, str) else bool(settings.MLS_RENTAL_APPLICATION))
        )
        top_limit = top_limit or int(settings.MLS_TOP_LIMIT)
        
        # OData expects true/false as lowercase, no quotes (as in working Postman)
        rental_application_str = str(rental_application_yn).lower()
        
        filter_query = (
            f"PropertyType eq '{property_type}' "
            f"and RentalApplicationYN eq {rental_application_str} "
            f"and OriginatingSystemName eq '{originating_system_name}'"
        )
        
        # Build the query string manually (no URL encoding for OData)
        query_string = (
            f"$filter={filter_query}"
            f"&$top={top_limit}"
            f"&$select={settings.MLS_PPROPERTY_FILTER_FIELDS}"
        )
        url = f"{self.mls_url}/Property?{query_string}"
        logger.info(f"MLS API request: {url}")
        logger.info(f"MLS API filter_query: {filter_query}")
        print(f"MLS API request: {url}")
        print(f"MLS API filter_query: {filter_query}")
        
        headers = {
            "Authorization": f"Bearer {self.mls_token}",
            "Content-Type": "application/json"
        }
        logger.info(f"MLS API headers: {headers}")
        print(f"MLS API headers: {headers}")
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        validated_response = MLSAPIResponse(**data)
                        return validated_response
                    else:
                        error_text = await response.text()
                        logger.error(f"MLS API error {response.status}: {error_text}")
                        print(f"MLS API error {response.status}: {error_text}")
                        raise MLSAPIError(
                            f"MLS API error: {response.status}",
                            response.status,
                            error_text
                        )
            except aiohttp.ClientError as e:
                logger.error(f"Network error connecting to MLS API: {e}")
                raise MLSAPIError(f"Network error connecting to MLS API: {e}", 503)
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise MLSAPIError(f"Unexpected error: {e}", 500)
    
    async def search_properties(self, params: PropertySearchParams) -> PropertyResponse:
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

    async def get_properties_selected_fields(self, top_limit: Optional[int] = None) -> MLSAPIResponse:
        """Get properties with only $select and $top filters (no $filter)."""
        if not self.mls_url or not self.mls_token:
            raise MLSAPIError("MLS configuration missing", 500)
        top_limit = top_limit or int(settings.MLS_TOP_LIMIT)
        query_string = (
            f"$select={settings.MLS_PPROPERTY_FILTER_FIELDS}"
            f"&$top={top_limit}"
        )
        url = f"{self.mls_url}/Property?{query_string}"
        logger.info(f"MLS API request (selected fields): {url}")
        print(f"MLS API request (selected fields): {url}")
        headers = {
            "Authorization": f"Bearer {self.mls_token}",
            "Content-Type": "application/json"
        }
        logger.info(f"MLS API headers: {headers}")
        print(f"MLS API headers: {headers}")
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        validated_response = MLSAPIResponse(**data)
                        return validated_response
                    else:
                        error_text = await response.text()
                        logger.error(f"MLS API error {response.status}: {error_text}")
                        print(f"MLS API error {response.status}: {error_text}")
                        raise MLSAPIError(
                            f"MLS API error: {response.status}",
                            response.status,
                            error_text
                        )
            except aiohttp.ClientError as e:
                logger.error(f"Network error connecting to MLS API: {e}")
                raise MLSAPIError(f"Network error connecting to MLS API: {e}", 503)
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise MLSAPIError(f"Unexpected error: {e}", 500)

property_service = PropertyService() 