from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional
from schemas.property import MLSAPIResponse, PropertyResponse, PropertyDetail, MediaResponse
from services.property_service import property_service, MLSAPIError
from core.dependencies import get_current_user
import logging
import urllib.parse

logger = logging.getLogger("mls_proxy")
logging.basicConfig(level=logging.INFO)

router = APIRouter(tags=["properties"])

@router.post("/search", response_model=MLSAPIResponse)
async def search_properties(
    property_type: Optional[str] = Query(None, description="Type of property (e.g., Residential Freehold)"),
    rental_application_yn: Optional[bool] = Query(None, description="Rental application required (true/false)"),
    top_limit: Optional[int] = Query(None, description="Maximum number of results to return")
):
    """Search for properties using MLS API with environment variables or dynamic query params"""
    try:
        return await property_service.search_properties_mls(
            property_type=property_type,
            rental_application_yn=rental_application_yn,
            top_limit=top_limit
        )
    except MLSAPIError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={"message": e.message, "external_detail": e.detail}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected server error occurred: {e}"
        )

@router.get("/get/{property_id}", response_model=PropertyDetail)
async def get_property(property_id: str):
    """Get specific property details"""
    try:
        return await property_service.get_property(property_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/media/{property_id}", response_model=MediaResponse)
async def get_property_media(property_id: str):
    """Get property media/images"""
    try:
        return await property_service.get_property_media(property_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) 