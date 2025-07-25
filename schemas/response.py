from pydantic import BaseModel
from typing import Optional, Any
from uuid import UUID
from datetime import datetime

class ResponseBase(BaseModel):
    user_id: Optional[UUID]
    question_id: Optional[UUID]
    selected_answer: Any  # JSONB
    flag_id: Optional[UUID]
    section: str

class ResponseCreate(ResponseBase):
    pass

class ResponseUpdate(BaseModel):
    user_id: Optional[UUID]
    question_id: Optional[UUID]
    selected_answer: Optional[Any]
    flag_id: Optional[UUID]
    section: Optional[str]

class Response(ResponseBase):
    id: UUID
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True 