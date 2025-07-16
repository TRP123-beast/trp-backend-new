from fastapi import APIRouter, HTTPException, status
from schemas.property import MLSAPIResponse, PropertyResponse, PropertyDetail, MediaResponse
from services.property_service import property_service, MLSAPIError
from core.dependencies import get_current_user

router = APIRouter(tags=["properties"])

@router.post("/search", response_model=MLSAPIResponse)
async def search_properties():
    """Search for properties using MLS API with environment variables"""
    try:
        return await property_service.search_properties_mls()
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