from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.exceptions import InvalidGeometryError, RegionNotFoundError
from app.database.database import get_db
from app.schemas.region import RegionCreate, RegionResponse
from app.services import region_service

router = APIRouter(prefix="/regions", tags=["regions"])


@router.post("/", response_model=RegionResponse, status_code=status.HTTP_201_CREATED)
def create_region(
    data: RegionCreate,
    db: Session = Depends(get_db),
) -> RegionResponse:
    try:
        return region_service.create_region(db, data)
    except InvalidGeometryError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid geometry",
        ) from exc


@router.get("/", response_model=list[RegionResponse])
def read_regions(db: Session = Depends(get_db)) -> list[RegionResponse]:
    return region_service.list_regions(db)


@router.get("/{region_id}", response_model=RegionResponse)
def read_region(
    region_id: int,
    db: Session = Depends(get_db),
) -> RegionResponse:
    try:
        return region_service.get_region(db, region_id)
    except RegionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Region not found",
        ) from exc
