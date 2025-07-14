from fastapi import APIRouter, HTTPException, Depends
from app.schemas.property import PropertyQuery, PropertyResponse, PropertyDetail, MediaResponse
from app.services.property_service import property_service
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/properties", tags=["properties"])

@router.post("/search", response_model=PropertyResponse)
async def search_properties(query: PropertyQuery):
    """Search for properties with filters"""
    try:
        return await property_service.search_properties(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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