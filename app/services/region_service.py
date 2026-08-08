from typing import Any

from shapely.errors import GEOSException
from shapely.geometry import shape
from sqlalchemy.orm import Session

from app.core.exceptions import InvalidGeometryError, RegionNotFoundError
from app.models.region import Region
from app.repositories import region_repository
from app.schemas.region import RegionCreate, RegionUpdate


def _validate_geometry(geometry: dict[str, Any]) -> None:
    try:
        geom = shape(geometry)
    except (ValueError, GEOSException) as exc:
        raise InvalidGeometryError from exc
    if not geom.is_valid:
        raise InvalidGeometryError


def list_regions(db: Session) -> list[Region]:
    return region_repository.get_all(db)


def get_region(db: Session, region_id: int) -> Region:
    region = region_repository.get_by_id(db, region_id)
    if region is None:
        raise RegionNotFoundError(region_id)
    return region


def create_region(db: Session, data: RegionCreate) -> Region:
    _validate_geometry(data.geometry)
    return region_repository.create(db, data)


def update_region(db: Session, region_id: int, data: RegionUpdate) -> Region:
    region = get_region(db, region_id)
    if data.geometry is not None:
        _validate_geometry(data.geometry)
    return region_repository.update(db, region, data)


def delete_region(db: Session, region_id: int) -> None:
    region = get_region(db, region_id)
    region_repository.delete(db, region)


def find_regions_containing_point(
    db: Session,
    latitude: float,
    longitude: float,
) -> list[Region]:
    return region_repository.find_containing_regions(db, latitude, longitude)


def find_regions_intersecting_point(
    db: Session,
    latitude: float,
    longitude: float,
) -> list[Region]:
    return region_repository.find_intersecting_regions(db, latitude, longitude)
