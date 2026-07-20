from pydantic import BaseModel


class GeoJSONUploadResponse(BaseModel):
    filename: str
    content_type: str
    size: int
    message: str
    feature_count: int
    columns: list[str]
    crs: str | None
    imported_ids: list[int]
