from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class FlagBase(BaseModel):
    flag_name: Optional[str]
    flag_number: Optional[int]

class FlagCreate(FlagBase):
    pass

class FlagUpdate(FlagBase):
    pass

class Flag(FlagBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True 