import io
import json
from pathlib import Path

import geopandas as gpd
from shapely.geometry import mapping
from sqlalchemy.orm import Session

from app.core.exceptions import InvalidGeoJSONFileError
from app.repositories import region_repository
from app.schemas.geojson_import import GeoJSONUploadResponse
from app.schemas.region import RegionCreate

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
_SUPPORTED_GEOMETRY_TYPES = frozenset({"Polygon", "MultiPolygon"})


_EXTENSION_ERROR = "Only .geojson and .json files are supported"
_CONTENT_TYPE_ERROR = "Content type must be application/json or application/geo+json"
_SIZE_ERROR = "File exceeds the maximum allowed size of 10 MB"
_JSON_DECODE_ERROR = "File is not valid JSON"
_GEOJSON_TYPE_ERROR = "Uploaded file must be a valid GeoJSON object"
_PARSE_ERROR = "Unable to parse GeoJSON with GeoPandas"
_CRS_ERROR = "Coordinate reference system could not be determined"
_UNSUPPORTED_GEOMETRY_ERROR = "Only Polygon and MultiPolygon geometries are supported"
_INVALID_GEOMETRY_ERROR = "GeoJSON contains invalid geometries"


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


def _parse_geodataframe(contents: bytes) -> gpd.GeoDataFrame:
    try:
        gdf = gpd.read_file(io.BytesIO(contents))
    except Exception as exc:
        raise InvalidGeoJSONFileError(_PARSE_ERROR) from exc

    if gdf.crs is None:
        raise InvalidGeoJSONFileError(_CRS_ERROR)

    return gdf.to_crs(epsg=4326)


def _validate_geometries(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    if gdf.geometry.isna().any():
        raise InvalidGeoJSONFileError(_INVALID_GEOMETRY_ERROR)

    if gdf.geometry.is_empty.any():
        raise InvalidGeoJSONFileError(_INVALID_GEOMETRY_ERROR)

    if not set(gdf.geom_type.unique()).issubset(_SUPPORTED_GEOMETRY_TYPES):
        raise InvalidGeoJSONFileError(_UNSUPPORTED_GEOMETRY_ERROR)

    if not gdf.is_valid.all():
        raise InvalidGeoJSONFileError(_INVALID_GEOMETRY_ERROR)

    return gdf


def _build_region_create_list(gdf: gpd.GeoDataFrame) -> list[RegionCreate]:
    creates = []
    for index, row in gdf.iterrows():
        properties = {k: v for k, v in row.items() if k != "geometry"}
        name = properties.get("name") or properties.get("Name") or f"Region_{index}"
        geometry = mapping(row.geometry)
        creates.append(RegionCreate(name=str(name), geometry=geometry))
    return creates


def process_geojson_upload(
    db: Session,
    filename: str,
    content_type: str,
    contents: bytes,
) -> GeoJSONUploadResponse:
    _validate_extension(filename)
    _validate_content_type(content_type)
    _validate_size(contents)
    _validate_geojson(contents)

    gdf = _validate_geometries(_parse_geodataframe(contents))

    region_creates = _build_region_create_list(gdf)
    regions = region_repository.create_many(db, region_creates)

    return GeoJSONUploadResponse(
        filename=filename,
        content_type=content_type,
        size=len(contents),
        message="GeoJSON file imported successfully",
        feature_count=len(gdf),
        columns=[column for column in gdf.columns if column != "geometry"],
        crs=str(gdf.crs) if gdf.crs else None,
        imported_ids=[region.id for region in regions],
    )
