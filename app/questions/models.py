from pydantic import BaseModel
from typing import Optional, Any
from uuid import UUID
from datetime import datetime

class QuestionBase(BaseModel):
    question_text: str
    answer_options: Any  # JSONB
    question_type: str
    section: str

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(BaseModel):
    question_text: Optional[str]
    answer_options: Optional[Any]
    question_type: Optional[str]
    section: Optional[str]

class Question(QuestionBase):
    id: UUID
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True 