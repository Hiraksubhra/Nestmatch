from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field


class CampusResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    short_name: Optional[str] = None
    city: str
    locality: Optional[str] = None
    latitude: float
    longitude: float


class CampusProximityItem(BaseModel):
    campus_id: str
    name: str
    short_name: Optional[str] = None
    city: Optional[str] = None
    locality: Optional[str] = None
    distance_km: float
    distance_meters: Optional[int] = None
    walking_time_mins: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class GeocodePreviewRequest(BaseModel):
    address_line1: Optional[str] = None
    locality: Optional[str] = None
    city: str
    pincode: Optional[str] = None


class GeocodePreviewResponse(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    formatted_address: Optional[str] = None
    nearby_campuses: List[CampusProximityItem] = []
