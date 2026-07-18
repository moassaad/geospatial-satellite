from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.core.exceptions import InvalidGeoJSONFileError
from app.schemas.geojson_import import GeoJSONUploadResponse
from app.services import geojson_import_service

router = APIRouter(prefix="/import", tags=["import"])


@router.post(
    "/geojson",
    response_model=GeoJSONUploadResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def upload_geojson(file: UploadFile = File(...)) -> GeoJSONUploadResponse:
    contents = await file.read()
    try:
        return geojson_import_service.process_geojson_upload(
            filename=file.filename or "",
            content_type=file.content_type or "",
            contents=contents,
        )
    except InvalidGeoJSONFileError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
