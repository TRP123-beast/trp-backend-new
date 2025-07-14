from pydantic import BaseModel, Field
from typing import Optional, List, Any

class PropertySearchParams(BaseModel):
    MLS_TOP_LIMIT: Optional[int] = 10
    MLS_RESOURCE_RECORD_KEY: Optional[str] = None
    MLS_PROPERTY_TYPE: Optional[str] = None
    MLS_RENTAL_APPLICATION: Optional[bool] = None
    MLS_ORIFINATING_SYSTEM_NAME: Optional[str] = None
    MLS_PPROPERTY_FILTER_FIELDS: Optional[str] = None

class PropertyBase(BaseModel):
    ListingKey: Optional[str] = None
    MLS_PROPERTY_TYPE: Optional[str] = None
    MLS_RENTAL_APPLICATION: Optional[str] = None
    MLS_ORIGINATING_SYSTEM_NAME: Optional[str] = None

class PropertyResponse(BaseModel):
    odata_context: str = Field(..., alias='@odata.context')
    value: List[Any]

class PropertyDetail(BaseModel):
    ListingKey: str
    ResourceRecordKey: Optional[str] = None
    # Add other property fields as needed
    
    class Config:
        from_attributes = True

class MediaQuery(BaseModel):
    property_id: str

class MediaResponse(BaseModel):
    property_id: str
    media_urls: List[str] 