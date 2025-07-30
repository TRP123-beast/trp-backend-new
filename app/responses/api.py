from fastapi import APIRouter, HTTPException
from typing import List
from uuid import UUID
from app.responses.models import Response, ResponseCreate, ResponseUpdate
from app.responses.services import response_service

router = APIRouter(tags=["responses"])

@router.get("/", response_model=List[Response])
def list_responses():
    try:
        return response_service.get_responses()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{response_id}", response_model=Response)
def get_response(response_id: UUID):
    try:
        return response_service.get_response(response_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=Response)
def create_response(response: ResponseCreate):
    try:
        return response_service.create_response(response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{response_id}", response_model=Response)
def update_response(response_id: UUID, response: ResponseUpdate):
    try:
        return response_service.update_response(response_id, response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{response_id}")
def delete_response(response_id: UUID):
    try:
        response_service.delete_response(response_id)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 