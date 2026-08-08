from datetime import datetime
from typing import Any

from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import to_shape
from pydantic import BaseModel, ConfigDict, Field, field_validator
from shapely.geometry import mapping

_EXAMPLE_GEOMETRY: dict[str, Any] = {
    "type": "Polygon",
    "coordinates": [
        [
            [31.0, 30.0],
            [31.5, 30.0],
            [31.5, 30.5],
            [31.0, 30.5],
            [31.0, 30.0],
        ]
    ],
}


class RegionBase(BaseModel):
    name: str = Field(examples=["Cairo"])
    geometry: dict[str, Any] = Field(examples=[_EXAMPLE_GEOMETRY])


class RegionCreate(RegionBase):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "Cairo",
                    "geometry": _EXAMPLE_GEOMETRY,
                }
            ],
        }
    )


class RegionUpdate(BaseModel):
    name: str | None = Field(default=None, examples=["Giza"])
    geometry: dict[str, Any] | None = Field(default=None, examples=[_EXAMPLE_GEOMETRY])

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "Giza",
                    "geometry": _EXAMPLE_GEOMETRY,
                }
            ],
        }
    )


class PointRequest(BaseModel):
    latitude: float
    longitude: float


class RegionResponse(RegionBase):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "name": "Cairo",
                    "geometry": _EXAMPLE_GEOMETRY,
                    "created_at": "2026-01-01T00:00:00",
                }
            ],
        },
    )

    id: int
    created_at: datetime

    @field_validator("geometry", mode="before")
    @classmethod
    def _convert_geometry(cls, value: Any) -> dict[str, Any]:
        if isinstance(value, WKBElement):
            return mapping(to_shape(value))
        return value
