from pydantic import BaseModel, ConfigDict


class GeoJSONUploadResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "filename": "regions.geojson",
                    "content_type": "application/geo+json",
                    "size": 2048,
                    "message": "GeoJSON file imported successfully",
                    "feature_count": 1,
                    "columns": ["name"],
                    "crs": "EPSG:4326",
                    "imported_ids": [1],
                }
            ],
        }
    )

    filename: str
    content_type: str
    size: int
    message: str
    feature_count: int
    columns: list[str]
    crs: str | None
    imported_ids: list[int]
