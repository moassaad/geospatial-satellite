from pydantic import BaseModel


class GeoJSONUploadResponse(BaseModel):
    filename: str
    content_type: str
    size: int
    message: str
