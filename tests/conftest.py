from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.database.database import get_db
from app.main import app
from app.models.region import Region


@pytest.fixture(autouse=True)
def _mock_repository():
    def side_effect(_db, data_list):
        if not data_list:
            return []
        return [
            Region(
                id=1,
                name=data_list[0].name,
                geometry={
                    "type": "Polygon",
                    "coordinates": [[[31.0, 30.0], [31.5, 30.0], [31.5, 30.5], [31.0, 30.5], [31.0, 30.0]]],
                },
                created_at=datetime.now(),
            )
        ]

    with patch("app.repositories.region_repository.create_many", side_effect=side_effect):
        yield


@pytest.fixture(autouse=True)
def _override_get_db():
    mock_session = MagicMock()
    app.dependency_overrides[get_db] = lambda: mock_session
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
