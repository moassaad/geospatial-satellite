from sqlalchemy.orm import Session

from app.repositories import health_repository
from app.schemas.health import HealthResponse, HealthStatus


def check_health(db: Session) -> HealthResponse:
    database_status = "ok" if health_repository.is_database_healthy(db) else "unhealthy"
    return HealthResponse(
        status="ok",
        database=HealthStatus(status=database_status),
    )
