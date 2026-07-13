from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.health import HealthResponse
from app.services import health_service

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", response_model=HealthResponse)
def health(db: Session = Depends(get_db)) -> HealthResponse:
    return health_service.check_health(db)
