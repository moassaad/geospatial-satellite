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


app = FastAPI(title=settings.app_name)
app.include_router(health_router)
app.include_router(region_router)
app.include_router(import_router)
app.include_router(spatial_router)


@app.get("/", response_model=RootResponse)
def read_root() -> RootResponse:
    return RootResponse(message="Hello World")
