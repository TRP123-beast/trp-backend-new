from pydantic import BaseModel, Field
from typing import Optional, List, Any

# Request models for FastAPI endpoints
class MLSPropertyQueryParams(BaseModel):
    """Query parameters for MLS property search"""
    property_type: Optional[str] = None
    rental_application_yn: Optional[bool] = None
    top_limit: Optional[int] = 100

# Response models for MLS API
class MLSPropertyDetails(BaseModel):
    """Individual property details from MLS API"""
    BathroomsTotalInteger: Optional[int] = None
    BedroomsTotal: Optional[int] = None
    BuildingAreaTotal: Optional[float] = None
    City: Optional[str] = None
    CityRegion: Optional[str] = None
    CrossStreet: Optional[str] = None
    ListingKey: str
    ListPrice: float = Field(..., ge=0)
    ParkingSpaces: Optional[int] = None
    UnparsedAddress: Optional[str] = None

class MLSAPIResponse(BaseModel):
    """Response structure from external MLS API"""
    odata_context: Optional[str] = Field(None, alias='@odata.context')
    value: List[MLSPropertyDetails]

# Legacy models (keeping for compatibility)
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
    
    class Config:
        from_attributes = True

class MediaQuery(BaseModel):
    property_id: str

class MediaResponse(BaseModel):
    property_id: str
    media_urls: List[str] 