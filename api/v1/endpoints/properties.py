from fastapi import APIRouter, HTTPException, status, Header
import os
import aiohttp
from schemas.property import PropertyResponse, PropertyDetail, MediaResponse
from services.property_service import property_service
from core.dependencies import get_current_user

router = APIRouter(tags=["properties"])

@router.post("/search")
async def search_properties(Authorization: str = Header(...)):
    mls_token = os.getenv("MLS_AUTHTOKEN")
    if not Authorization.startswith("Bearer ") or Authorization.split(" ", 1)[1] != mls_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token")

    MLS_URL = os.getenv("MLS_URL")
    MLS_PROPERTY_TYPE = os.getenv("MLS_PROPERTY_TYPE")
    MLS_RENTAL_APPLICATION = os.getenv("MLS_RENTAL_APPLICATION")
    MLS_ORIFINATING_SYSTEM_NAME = os.getenv("MLS_ORIFINATING_SYSTEM_NAME")
    MLS_TOP_LIMIT = os.getenv("MLS_TOP_LIMIT")
    MLS_PPROPERTY_FILTER_FIELDS = os.getenv("MLS_PPROPERTY_FILTER_FIELDS")

    url = (
        f"{MLS_URL}/Property?"
        f"$filter=PropertyType eq '{MLS_PROPERTY_TYPE}' and RentalApplicationYN eq {MLS_RENTAL_APPLICATION} "
        f"and OriginatingSystemName eq '{MLS_ORIFINATING_SYSTEM_NAME}'"
        f"&$top={MLS_TOP_LIMIT}"
        f"&$select={MLS_PPROPERTY_FILTER_FIELDS}"
    )

    headers = {
        "Authorization": f"Bearer {mls_token}"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                raise HTTPException(status_code=resp.status, detail=await resp.text())
            return await resp.json()

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