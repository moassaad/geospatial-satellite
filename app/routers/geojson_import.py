from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.exceptions import InvalidGeoJSONFileError
from app.database.database import get_db
from app.schemas.geojson_import import GeoJSONUploadResponse
from app.services import geojson_import_service

router = APIRouter(prefix="/import", tags=["import"])


@router.post(
    "/geojson",
    response_model=GeoJSONUploadResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Invalid or unsupported GeoJSON file",
        },
    },
)
async def upload_geojson(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> GeoJSONUploadResponse:
    contents = await file.read()
    try:
        return geojson_import_service.process_geojson_upload(
            db=db,
            filename=file.filename or "",
            content_type=file.content_type or "",
            contents=contents,
        )
    except InvalidGeoJSONFileError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
