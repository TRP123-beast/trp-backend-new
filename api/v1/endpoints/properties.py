from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional
from schemas.property import MLSAPIResponse, PropertyResponse, PropertyDetail, MediaResponse
from services.property_service import property_service, MLSAPIError
from core.dependencies import get_current_user
from core.config import settings
import logging
import urllib.parse

logger = logging.getLogger("mls_proxy")
logging.basicConfig(level=logging.INFO)

router = APIRouter(tags=["properties"])

@router.get("/search", response_model=MLSAPIResponse)
async def search_properties(
    property_type: Optional[str] = Query(None, description="Type of property (e.g., Residential Freehold)"),
    rental_application_yn: Optional[bool] = Query(None, description="Rental application required (true/false)"),
    top_limit: Optional[int] = Query(None, description="Maximum number of results to return"),
    originating_system_name: Optional[str] = Query(None, description="Originating System Name (e.g., Toronto Regional Real Estate Board)")
):
    """Search for properties using MLS API with environment variables or dynamic query params"""
    try:
        return await property_service.search_properties_mls(
            property_type=property_type,
            rental_application_yn=rental_application_yn,
            top_limit=top_limit,
            originating_system_name=originating_system_name
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

@router.get("/selected-fields", response_model=MLSAPIResponse, summary="Get Properties with Selected Fields")
async def get_properties_selected_fields(
    top_limit: Optional[int] = Query(None, description="Maximum number of results to return")
):
    """Get properties with only $select and $top filters (no $filter)."""
    try:
        return await property_service.get_properties_selected_fields(top_limit=top_limit)
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

@router.get("/media/{property_id}", response_model=MediaResponse, summary="Get Property Images with Selected Fields")
async def get_property_media_with_fields(property_id: str):
    """Get property media/images with selected fields filter"""
    try:
        return await property_service.get_property_media(property_id)
    except MLSAPIError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={"message": e.message, "external_detail": e.detail}
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/media-simple/{property_id}", response_model=MediaResponse, summary="Get Property Images")
async def get_property_media_simple(property_id: str):
    """Get property media/images with minimal filters - just ResourceRecordKey filter"""
    try:
        return await property_service.get_property_media_simple(property_id)
    except MLSAPIError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={"message": e.message, "external_detail": e.detail}
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) 