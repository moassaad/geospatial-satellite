import io

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.core.exceptions import InvalidGeoJSONFileError
from app.schemas.geojson_import import GeoJSONUploadResponse
from app.services import geojson_import_service

VALID_CONTENT_TYPE = "application/geo+json"
VALID_FILENAME = "regions.geojson"

def _valid_geojson_bytes() -> bytes:
    payload = b'{"type": "FeatureCollection", "features": []}'
    return payload


class TestProcessGeojsonUpload:
    def test_valid_upload(self) -> None:
        response = geojson_import_service.process_geojson_upload(
            filename=VALID_FILENAME,
            content_type=VALID_CONTENT_TYPE,
            contents=_valid_geojson_bytes(),
        )
        assert isinstance(response, GeoJSONUploadResponse)
        assert response.filename == VALID_FILENAME
        assert response.content_type == VALID_CONTENT_TYPE
        assert response.size == len(_valid_geojson_bytes())
        assert response.message == "GeoJSON file accepted for import"

    def test_rejects_unsupported_extension(self) -> None:
        with pytest.raises(InvalidGeoJSONFileError):
            geojson_import_service.process_geojson_upload(
                filename="data.txt",
                content_type=VALID_CONTENT_TYPE,
                contents=_valid_geojson_bytes(),
            )

    def test_rejects_unsupported_content_type(self) -> None:
        with pytest.raises(InvalidGeoJSONFileError):
            geojson_import_service.process_geojson_upload(
                filename=VALID_FILENAME,
                content_type="text/plain",
                contents=_valid_geojson_bytes(),
            )

    def test_rejects_oversized_file(self) -> None:
        large = b"x" * (10 * 1024 * 1024 + 1)
        with pytest.raises(InvalidGeoJSONFileError):
            geojson_import_service.process_geojson_upload(
                filename=VALID_FILENAME,
                content_type=VALID_CONTENT_TYPE,
                contents=large,
            )

    def test_rejects_invalid_json(self) -> None:
        with pytest.raises(InvalidGeoJSONFileError):
            geojson_import_service.process_geojson_upload(
                filename=VALID_FILENAME,
                content_type=VALID_CONTENT_TYPE,
                contents=b"not json",
            )

    def test_rejects_non_geojson_object(self) -> None:
        with pytest.raises(InvalidGeoJSONFileError):
            geojson_import_service.process_geojson_upload(
                filename=VALID_FILENAME,
                content_type=VALID_CONTENT_TYPE,
                contents=b'{"type": "unknown"}',
            )

    def test_rejects_array(self) -> None:
        with pytest.raises(InvalidGeoJSONFileError):
            geojson_import_service.process_geojson_upload(
                filename=VALID_FILENAME,
                content_type=VALID_CONTENT_TYPE,
                contents=b"[1, 2, 3]",
            )

    def test_rejects_primitive(self) -> None:
        with pytest.raises(InvalidGeoJSONFileError):
            geojson_import_service.process_geojson_upload(
                filename=VALID_FILENAME,
                content_type=VALID_CONTENT_TYPE,
                contents=b'"string"',
            )

    def test_accepts_json_extension(self) -> None:
        response = geojson_import_service.process_geojson_upload(
            filename="data.json",
            content_type="application/json",
            contents=_valid_geojson_bytes(),
        )
        assert response.filename == "data.json"

    def test_empty_filename(self) -> None:
        with pytest.raises(InvalidGeoJSONFileError):
            geojson_import_service.process_geojson_upload(
                filename="",
                content_type=VALID_CONTENT_TYPE,
                contents=_valid_geojson_bytes(),
            )

    def test_empty_content_type(self) -> None:
        with pytest.raises(InvalidGeoJSONFileError):
            geojson_import_service.process_geojson_upload(
                filename=VALID_FILENAME,
                content_type="",
                contents=_valid_geojson_bytes(),
            )


class TestUploadEndpoint:
    def test_returns_202_and_metadata(self, client: TestClient) -> None:
        response = client.post(
            "/import/geojson",
            files={"file": (VALID_FILENAME, _valid_geojson_bytes(), VALID_CONTENT_TYPE)},
        )
        assert response.status_code == status.HTTP_202_ACCEPTED
        data = response.json()
        assert data["filename"] == VALID_FILENAME
        assert data["content_type"] == VALID_CONTENT_TYPE
        assert data["size"] == len(_valid_geojson_bytes())
        assert data["message"] == "GeoJSON file accepted for import"

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
