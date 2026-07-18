import json
from pathlib import Path

from app.core.exceptions import InvalidGeoJSONFileError
from app.schemas.geojson_import import GeoJSONUploadResponse

_MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024
_ALLOWED_EXTENSIONS = frozenset({".geojson", ".json"})
_ALLOWED_CONTENT_TYPES = frozenset({"application/json", "application/geo+json"})
_GEOJSON_TYPES = frozenset({
    "FeatureCollection",
    "Feature",
    "Point",
    "MultiPoint",
    "LineString",
    "MultiLineString",
    "Polygon",
    "MultiPolygon",
    "GeometryCollection",
})


_EXTENSION_ERROR = "Only .geojson and .json files are supported"
_CONTENT_TYPE_ERROR = "Content type must be application/json or application/geo+json"
_SIZE_ERROR = "File exceeds the maximum allowed size of 10 MB"
_JSON_DECODE_ERROR = "File is not valid JSON"
_GEOJSON_TYPE_ERROR = "Uploaded file must be a valid GeoJSON object"


def _validate_extension(filename: str) -> None:
    extension = Path(filename).suffix.lower()
    if extension not in _ALLOWED_EXTENSIONS:
        raise InvalidGeoJSONFileError(_EXTENSION_ERROR)


def _validate_content_type(content_type: str) -> None:
    if content_type.lower() not in _ALLOWED_CONTENT_TYPES:
        raise InvalidGeoJSONFileError(_CONTENT_TYPE_ERROR)


def _validate_size(contents: bytes) -> None:
    if len(contents) > _MAX_FILE_SIZE_BYTES:
        raise InvalidGeoJSONFileError(_SIZE_ERROR)


def _validate_geojson(contents: bytes) -> None:
    try:
        geojson = json.loads(contents.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise InvalidGeoJSONFileError(_JSON_DECODE_ERROR) from exc

    if not isinstance(geojson, dict) or geojson.get("type") not in _GEOJSON_TYPES:
        raise InvalidGeoJSONFileError(_GEOJSON_TYPE_ERROR)


def process_geojson_upload(
    filename: str,
    content_type: str,
    contents: bytes,
) -> GeoJSONUploadResponse:
    _validate_extension(filename)
    _validate_content_type(content_type)
    _validate_size(contents)
    _validate_geojson(contents)

    return GeoJSONUploadResponse(
        filename=filename,
        content_type=content_type,
        size=len(contents),
        message="GeoJSON file accepted for import",
    )
