from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.region import PointRequest, RegionResponse
from app.services import region_service

router = APIRouter(tags=["spatial"])


@router.post("/contains", response_model=list[RegionResponse])
def contains(
    data: PointRequest,
    db: Session = Depends(get_db),
) -> list[RegionResponse]:
    return region_service.find_regions_containing_point(
        db,
        data.latitude,
        data.longitude,
    )
