from sqlalchemy import func, select
from sqlalchemy.orm import Session
from geoalchemy2.shape import from_shape
from shapely.geometry import shape

from app.models.region import Region
from app.schemas.region import RegionCreate, RegionUpdate


def get_all(db: Session) -> list[Region]:
    return db.execute(select(Region)).scalars().all()


def get_by_id(db: Session, region_id: int) -> Region | None:
    return db.execute(
        select(Region).where(Region.id == region_id),
    ).scalars().first()


def create(db: Session, data: RegionCreate) -> Region:
    geometry = from_shape(shape(data.geometry), srid=4326)
    region = Region(
        name=data.name,
        geometry=geometry,
    )
    db.add(region)
    db.commit()
    db.refresh(region)
    return region


def create_many(db: Session, data_list: list[RegionCreate]) -> list[Region]:
    regions = []
    for data in data_list:
        geometry = from_shape(shape(data.geometry), srid=4326)
        region = Region(
            name=data.name,
            geometry=geometry,
        )
        regions.append(region)
    db.add_all(regions)
    db.commit()
    for region in regions:
        db.refresh(region)
    return regions


def update(db: Session, region: Region, data: RegionUpdate) -> Region:
    if data.name is not None:
        region.name = data.name
    if data.geometry is not None:
        region.geometry = from_shape(shape(data.geometry), srid=4326)
    db.commit()
    db.refresh(region)
    return region


def delete(db: Session, region: Region) -> None:
    db.delete(region)
    db.commit()


def find_containing_regions(
    db: Session,
    latitude: float,
    longitude: float,
) -> list[Region]:
    point = func.ST_GeomFromText(f"POINT({longitude} {latitude})", 4326)
    statement = select(Region).where(func.ST_Contains(Region.geometry, point))
    return db.execute(statement).scalars().all()


def find_intersecting_regions(
    db: Session,
    latitude: float,
    longitude: float,
) -> list[Region]:
    point = func.ST_GeomFromText(f"POINT({longitude} {latitude})", 4326)
    statement = select(Region).where(func.ST_Intersects(Region.geometry, point))
    return db.execute(statement).scalars().all()
