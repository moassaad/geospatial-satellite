from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class RegionBase(BaseModel):
    name: str
    geometry: dict[str, Any]


class RegionCreate(RegionBase):
    pass


class RegionUpdate(BaseModel):
    name: str | None = None
    geometry: dict[str, Any] | None = None


class RegionResponse(RegionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
