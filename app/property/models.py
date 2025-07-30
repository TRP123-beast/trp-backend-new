from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime
from uuid import UUID

# MLS API Response Models
class MLSAPIResponse(BaseModel):
    odata_context: Optional[str] = None
    value: List[dict] = []

class MLSPropertyDetails(BaseModel):
    BathroomsTotalInteger: Optional[int] = None
    BedroomsTotal: Optional[int] = None
    BuildingAreaTotal: Optional[float] = None
    City: Optional[str] = None
    CityRegion: Optional[str] = None
    CrossStreet: Optional[str] = None
    ListingKey: str
    ListPrice: Optional[float] = None
    ParkingSpaces: Optional[int] = None
    UnparsedAddress: Optional[str] = None

# Property Search Models
class PropertySearchParams(BaseModel):
    MLS_PROPERTY_TYPE: Optional[str] = None
    MLS_RENTAL_APPLICATION: Optional[bool] = None
    MLS_ORIFINATING_SYSTEM_NAME: Optional[str] = None
    MLS_TOP_LIMIT: int = 10
    MLS_PPROPERTY_FILTER_FIELDS: Optional[str] = None

class PropertyResponse(BaseModel):
    odata_context: str
    value: List[dict]

class PropertyDetail(BaseModel):
    BathroomsTotalInteger: Optional[int] = None
    BedroomsTotal: Optional[int] = None
    BuildingAreaTotal: Optional[float] = None
    City: Optional[str] = None
    CityRegion: Optional[str] = None
    CrossStreet: Optional[str] = None
    ListingKey: str
    ListPrice: Optional[float] = None
    ParkingSpaces: Optional[int] = None
    UnparsedAddress: Optional[str] = None

# Media Models
class MediaResponse(BaseModel):
    property_id: str
    media_urls: List[str] 