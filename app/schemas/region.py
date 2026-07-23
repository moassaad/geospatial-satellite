from datetime import datetime
from typing import Any

from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import to_shape
from pydantic import BaseModel, ConfigDict, field_validator
from shapely.geometry import mapping


class RegionBase(BaseModel):
    name: str
    geometry: dict[str, Any]


class RegionCreate(RegionBase):
    pass


class RegionUpdate(BaseModel):
    name: str | None = None
    geometry: dict[str, Any] | None = None


class PointRequest(BaseModel):
    latitude: float
    longitude: float


class RegionResponse(RegionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime

    @field_validator("geometry", mode="before")
    @classmethod
    def _convert_geometry(cls, value: Any) -> dict[str, Any]:
        if isinstance(value, WKBElement):
            return mapping(to_shape(value))
        return value
