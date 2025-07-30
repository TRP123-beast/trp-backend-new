from pydantic import BaseModel
from typing import Optional, Any
from uuid import UUID
from datetime import datetime

class ResponseBase(BaseModel):
    question_id: UUID
    user_id: UUID
    selected_answer: Any  # JSONB
    response_text: Optional[str]

class ResponseCreate(ResponseBase):
    pass

class ResponseUpdate(BaseModel):
    question_id: Optional[UUID]
    user_id: Optional[UUID]
    selected_answer: Optional[Any]
    response_text: Optional[str]

class Response(ResponseBase):
    id: UUID
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True 