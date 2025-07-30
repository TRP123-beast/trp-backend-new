import aiohttp
from typing import Optional, Dict, Any
from core.config import settings
from app.property.models import MLSAPIResponse, PropertyDetail, MediaResponse
import logging

logger = logging.getLogger("mls_proxy")

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

class MLSClient:
    def __init__(self):
        self.mls_url = settings.MLS_URL
        self.mls_token = settings.MLS_AUTHTOKEN

    async def _make_mls_get_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        A private helper method to handle basic MLS GET requests.
        Ensures consistent headers, error handling, and uses the params dictionary.
        """
        if not self.mls_url or not self.mls_token:
            raise MLSAPIError("MLS configuration missing", 500)

        url = f"{self.mls_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.mls_token}"}
        
        # Log the request details for debugging
        logger.info(f"Making external MLS GET request to: {url}")
        logger.info(f"Request params: {params}")
        print(f"Making external MLS GET request to: {url}")
        print(f"Request params: {params}")
        
        # Log the full URL that will be constructed
        if params:
            import urllib.parse
            query_string = urllib.parse.urlencode(params)
            full_url = f"{url}?{query_string}"
            logger.info(f"Full URL being sent: {full_url}")
            print(f"Full URL being sent: {full_url}")
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers, params=params, timeout=30) as response:
                    response_text = await response.text()
                    print(f"MLS API response status: {response.status}")
                    print(f"MLS API response text: {response_text}")
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"MLS API error {response.status}: {response_text}")
                        # Attempt to parse JSON error message if available
                        error_detail = None
                        try:
                            error_json = response.json()
                            error_detail = error_json.get("error", {}).get("message", response_text)
                        except aiohttp.ContentTypeError:
                            error_detail = response_text
                        
                        raise MLSAPIError(
                            f"External API returned an error: {response.status}",
                            response.status,
                            error_detail
                        )
            except aiohttp.ClientError as e:
                logger.error(f"Network error connecting to MLS API: {e}")
                raise MLSAPIError(f"Network error: {e}", 503)
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise MLSAPIError(f"Unexpected error: {e}", 500)

    async def search_properties_by_filters(self, filters: str, top_limit: int, select_fields: str) -> MLSAPIResponse:
        """
        Gets properties based on a flexible filter string.
        Args:
            filters: The OData filter string, e.g., "PropertyType eq 'Residential' and ListPrice gt 500000"
            top_limit: The maximum number of results.
            select_fields: A comma-separated list of fields to return.
        """
        params = {
            "$filter": filters,
            "$top": top_limit,
            "$select": select_fields
        }
        data = await self._make_mls_get_request(endpoint="Property", params=params)
        return MLSAPIResponse(**data)

    async def get_properties_with_selected_fields(self, top_limit: int, select_fields: str) -> MLSAPIResponse:
        """
        Gets properties with only $select and $top filters.
        """
        params = {
            "$top": top_limit,
            "$select": select_fields
        }
        data = await self._make_mls_get_request(endpoint="Property", params=params)
        return MLSAPIResponse(**data)
    
    async def get_property_by_id(self, listing_key: str, select_fields: str) -> PropertyDetail:
        """
        Gets a single property's details by its ListingKey.
        """
        params = {
            "$filter": f"ListingKey eq '{listing_key}'",
            "$select": select_fields
        }
        data = await self._make_mls_get_request(endpoint="Property", params=params)
        # Assuming the response is a list with a single item
        if data and "value" in data and data["value"]:
            return PropertyDetail(**data["value"][0])
        raise MLSAPIError(f"Property with ListingKey '{listing_key}' not found", 404)

    async def get_property_media_simple(self, resource_record_key: str) -> MediaResponse:
        """
        Gets a property's media (images) using its ResourceRecordKey.
        """
        params = {
            "$filter": f"ResourceRecordKey eq '{resource_record_key}'"
        }
        data = await self._make_mls_get_request(endpoint="Media", params=params)
        
        media_urls = [item.get("MediaURL") for item in data.get("value", []) if item.get("MediaURL")]
        return MediaResponse(
            property_id=resource_record_key,
            media_urls=media_urls
        )

    async def get_property_media_with_fields(self, resource_record_key: str, select_fields: str) -> MediaResponse:
        """
        Gets property media with a specific set of fields.
        """
        params = {
            "$filter": f"ResourceRecordKey eq '{resource_record_key}'",
            "$select": select_fields
        }
        data = await self._make_mls_get_request(endpoint="Media", params=params)
        
        media_urls = [item.get("MediaURL") for item in data.get("value", []) if item.get("MediaURL")]
        return MediaResponse(
            property_id=resource_record_key,
            media_urls=media_urls
        )

mls_client = MLSClient() 