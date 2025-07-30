from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional
from app.property.models import MLSAPIResponse, PropertyResponse, PropertyDetail, MediaResponse
from app.property.clients import mls_client, MLSAPIError
from app.auth.deps import get_current_user
from core.config import settings
import logging

logger = logging.getLogger("mls_proxy")

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
        # Build filter string from parameters - temporarily exclude boolean to test
        filters = []
        if property_type:
            filters.append(f"PropertyType eq '{property_type}'")
        # Temporarily comment out boolean filter to isolate the issue
        # if rental_application_yn is not None:
        #     # Try different boolean formats - some OData APIs are picky about boolean syntax
        #     if rental_application_yn:
        #         filters.append("RentalApplicationYN eq true")
        #     else:
        #         filters.append("RentalApplicationYN eq false")
        if originating_system_name:
            filters.append(f"OriginatingSystemName eq '{originating_system_name}'")
        
        filter_string = " and ".join(filters) if filters else None
        top_limit = top_limit or int(settings.MLS_TOP_LIMIT)
        select_fields = settings.MLS_PPROPERTY_FILTER_FIELDS
        
        if filter_string:
            return await mls_client.search_properties_by_filters(
                filters=filter_string,
                top_limit=top_limit,
                select_fields=select_fields
            )
        else:
            return await mls_client.get_properties_with_selected_fields(
                top_limit=top_limit,
                select_fields=select_fields
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
        top_limit = top_limit or int(settings.MLS_TOP_LIMIT)
        select_fields = settings.MLS_PPROPERTY_FILTER_FIELDS
        return await mls_client.get_properties_with_selected_fields(
            top_limit=top_limit,
            select_fields=select_fields
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
        select_fields = settings.MLS_PPROPERTY_FILTER_FIELDS
        return await mls_client.get_property_by_id(property_id, select_fields)
    except MLSAPIError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={"message": e.message, "external_detail": e.detail}
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/media/{property_id}", response_model=MediaResponse, summary="Get Property Images with Selected Fields")
async def get_property_media_with_fields(property_id: str):
    """Get property media/images with selected fields filter"""
    try:
        select_fields = getattr(settings, 'MLS_PROPERTY_IMAGE_FILTER_FIELDS', 
            'ImageHeight,ImageSizeDescription,ImageWidth,MediaKey,MediaObjectID,MediaType,MediaURL,Order,ResourceRecordKey')
        return await mls_client.get_property_media_with_fields(property_id, select_fields)
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
        return await mls_client.get_property_media_simple(property_id)
    except MLSAPIError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={"message": e.message, "external_detail": e.detail}
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) 