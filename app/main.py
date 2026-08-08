from pydantic import BaseModel
from fastapi import FastAPI

from app.config.settings import Settings
from app.routers.geojson_import import router as import_router
from app.routers.health import router as health_router
from app.routers.region import router as region_router
from app.routers.spatial import router as spatial_router

settings = Settings()


class RootResponse(BaseModel):
    message: str


openapi_tags = [
    {
        "name": "health",
        "description": "Health status of the application and its database.",
    },
    {
        "name": "regions",
        "description": "Create, read, update, and delete Regions of Interest.",
    },
    {
        "name": "import",
        "description": "Import GeoJSON files into the region catalog.",
    },
]


app = FastAPI(title=settings.app_name, openapi_tags=openapi_tags)
app.include_router(health_router)
app.include_router(region_router)
app.include_router(import_router)
app.include_router(spatial_router)


@app.get("/", response_model=RootResponse)
def read_root() -> RootResponse:
    return RootResponse(message="Hello World")
