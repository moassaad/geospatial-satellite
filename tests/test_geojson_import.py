import json
from unittest.mock import MagicMock

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.core.exceptions import InvalidGeoJSONFileError
from app.schemas.geojson_import import GeoJSONUploadResponse
from app.services import geojson_import_service

VALID_CONTENT_TYPE = "application/geo+json"
VALID_FILENAME = "regions.geojson"


def _empty_geojson_bytes() -> bytes:
    return b'{"type": "FeatureCollection", "features": []}'


def _polygon_geojson_bytes() -> bytes:
    return json.dumps({
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Cairo"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[31.0, 30.0], [31.5, 30.0], [31.5, 30.5], [31.0, 30.5], [31.0, 30.0]]],
                },
            }
        ],
    }).encode()


def _point_geojson_bytes() -> bytes:
    return json.dumps({
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {"type": "Point", "coordinates": [31.0, 30.0]},
            }
        ],
    }).encode()


class TestProcessGeojsonUpload:
    def test_valid_upload(self) -> None:
        db = MagicMock()
        response = geojson_import_service.process_geojson_upload(
            db=db,
            filename=VALID_FILENAME,
            content_type=VALID_CONTENT_TYPE,
            contents=_polygon_geojson_bytes(),
        )
        assert isinstance(response, GeoJSONUploadResponse)
        assert response.filename == VALID_FILENAME
        assert response.content_type == VALID_CONTENT_TYPE
        assert response.size == len(_polygon_geojson_bytes())
        assert response.message == "GeoJSON file imported successfully"
        assert response.feature_count == 1
        assert response.columns == ["name"]
        assert response.crs == "EPSG:4326"
        assert response.imported_ids == [1]

    def test_empty_feature_collection(self) -> None:
        db = MagicMock()
        response = geojson_import_service.process_geojson_upload(
            db=db,
            filename=VALID_FILENAME,
            content_type=VALID_CONTENT_TYPE,
            contents=_empty_geojson_bytes(),
        )
        assert response.feature_count == 0
        assert response.columns == []
        assert response.crs == "EPSG:4326"
        assert response.imported_ids == []

    def test_rejects_unsupported_extension(self) -> None:
        db = MagicMock()
        with pytest.raises(InvalidGeoJSONFileError):
            geojson_import_service.process_geojson_upload(
                db=db,
                filename="data.txt",
                content_type=VALID_CONTENT_TYPE,
                contents=_empty_geojson_bytes(),
            )

    def test_rejects_unsupported_content_type(self) -> None:
        db = MagicMock()
        with pytest.raises(InvalidGeoJSONFileError):
            geojson_import_service.process_geojson_upload(
                db=db,
                filename=VALID_FILENAME,
                content_type="text/plain",
                contents=_empty_geojson_bytes(),
            )

    def test_rejects_oversized_file(self) -> None:
        db = MagicMock()
        large = b"x" * (10 * 1024 * 1024 + 1)
        with pytest.raises(InvalidGeoJSONFileError):
            geojson_import_service.process_geojson_upload(
                db=db,
                filename=VALID_FILENAME,
                content_type=VALID_CONTENT_TYPE,
                contents=large,
            )

    def test_rejects_invalid_json(self) -> None:
        db = MagicMock()
        with pytest.raises(InvalidGeoJSONFileError):
            geojson_import_service.process_geojson_upload(
                db=db,
                filename=VALID_FILENAME,
                content_type=VALID_CONTENT_TYPE,
                contents=b"not json",
            )

    def test_rejects_non_geojson_object(self) -> None:
        db = MagicMock()
        with pytest.raises(InvalidGeoJSONFileError):
            geojson_import_service.process_geojson_upload(
                db=db,
                filename=VALID_FILENAME,
                content_type=VALID_CONTENT_TYPE,
                contents=b'{"type": "unknown"}',
            )

    def test_rejects_array(self) -> None:
        db = MagicMock()
        with pytest.raises(InvalidGeoJSONFileError):
            geojson_import_service.process_geojson_upload(
                db=db,
                filename=VALID_FILENAME,
                content_type=VALID_CONTENT_TYPE,
                contents=b"[1, 2, 3]",
            )

    def test_rejects_primitive(self) -> None:
        db = MagicMock()
        with pytest.raises(InvalidGeoJSONFileError):
            geojson_import_service.process_geojson_upload(
                db=db,
                filename=VALID_FILENAME,
                content_type=VALID_CONTENT_TYPE,
                contents=b'"string"',
            )

    def test_accepts_json_extension(self) -> None:
        db = MagicMock()
        response = geojson_import_service.process_geojson_upload(
            db=db,
            filename="data.json",
            content_type="application/json",
            contents=_polygon_geojson_bytes(),
        )
        assert response.filename == "data.json"

    def test_empty_filename(self) -> None:
        db = MagicMock()
        with pytest.raises(InvalidGeoJSONFileError):
            geojson_import_service.process_geojson_upload(
                db=db,
                filename="",
                content_type=VALID_CONTENT_TYPE,
                contents=_empty_geojson_bytes(),
            )

    def test_empty_content_type(self) -> None:
        db = MagicMock()
        with pytest.raises(InvalidGeoJSONFileError):
            geojson_import_service.process_geojson_upload(
                db=db,
                filename=VALID_FILENAME,
                content_type="",
                contents=_empty_geojson_bytes(),
            )

    def test_rejects_point_geometry(self) -> None:
        db = MagicMock()
        with pytest.raises(InvalidGeoJSONFileError):
            geojson_import_service.process_geojson_upload(
                db=db,
                filename=VALID_FILENAME,
                content_type=VALID_CONTENT_TYPE,
                contents=_point_geojson_bytes(),
            )


class TestUploadEndpoint:
    def test_returns_201_and_metadata(self, client: TestClient) -> None:
        response = client.post(
            "/import/geojson",
            files={"file": (VALID_FILENAME, _polygon_geojson_bytes(), VALID_CONTENT_TYPE)},
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["filename"] == VALID_FILENAME
        assert data["content_type"] == VALID_CONTENT_TYPE
        assert data["size"] == len(_polygon_geojson_bytes())
        assert data["message"] == "GeoJSON file imported successfully"
        assert data["feature_count"] == 1
        assert data["columns"] == ["name"]
        assert data["crs"] == "EPSG:4326"
        assert data["imported_ids"] == [1]

    @pytest.mark.parametrize(
        ("filename", "content_type", "body"),
        [
            ("data.txt", VALID_CONTENT_TYPE, b'{"type": "FeatureCollection"}'),
            (VALID_FILENAME, "text/plain", b'{"type": "FeatureCollection"}'),
            (VALID_FILENAME, VALID_CONTENT_TYPE, b"not json"),
        ],
    )
    def test_returns_422_on_invalid_input(
        self,
        client: TestClient,
        filename: str,
        content_type: str,
        body: bytes,
    ) -> None:
        response = client.post(
            "/import/geojson",
            files={"file": (filename, body, content_type)},
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
