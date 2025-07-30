from fastapi import APIRouter, HTTPException
from typing import List
from uuid import UUID
from app.flags.models import Flag, FlagCreate, FlagUpdate
from app.flags.services import flag_service

router = APIRouter(tags=["flags"])

@router.get("/", response_model=List[Flag])
def list_flags():
    try:
        return flag_service.get_flags()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{flag_id}", response_model=Flag)
def get_flag(flag_id: UUID):
    try:
        return flag_service.get_flag(flag_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=Flag)
def create_flag(flag: FlagCreate):
    try:
        return flag_service.create_flag(flag)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{flag_id}", response_model=Flag)
def update_flag(flag_id: UUID, flag: FlagUpdate):
    try:
        return flag_service.update_flag(flag_id, flag)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{flag_id}")
def delete_flag(flag_id: UUID):
    try:
        flag_service.delete_flag(flag_id)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 