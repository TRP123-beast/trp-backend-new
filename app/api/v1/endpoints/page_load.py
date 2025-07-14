from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from app.services.page_load_service import page_load_service
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/page_load", tags=["page_load"])

@router.get("/home")
async def get_home_data(current_user: Optional[dict] = Depends(get_current_user)):
    """Get merged data for home page load"""
    try:
        user_info = current_user if current_user else None
        return await page_load_service.get_home_data(user_info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 