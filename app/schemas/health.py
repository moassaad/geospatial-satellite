from pydantic import BaseModel, ConfigDict


class HealthStatus(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "status": "ok",
                }
            ],
        }
    )

    status: str


class HealthResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "status": "ok",
                    "database": {
                        "status": "ok",
                    },
                }
            ],
        }
    )

    status: str
    database: HealthStatus
