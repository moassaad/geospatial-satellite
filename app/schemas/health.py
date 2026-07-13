from pydantic import BaseModel


class HealthStatus(BaseModel):
    status: str


class HealthResponse(BaseModel):
    status: str
    database: HealthStatus
