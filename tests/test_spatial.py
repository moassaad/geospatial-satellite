from datetime import datetime, timezone
from unittest.mock import MagicMock

from fastapi import status

from app.models.region import Region
from app.repositories import region_repository
from app.services import region_service


def test_intersects_endpoint_returns_regions(client, monkeypatch) -> None:
    expected_regions = [
        Region(
            id=1,
            name="Cairo",
            geometry={
                "type": "Polygon",
                "coordinates": [[[31.0, 30.0], [31.5, 30.0], [31.5, 30.5], [31.0, 30.5], [31.0, 30.0]]],
            },
            created_at=datetime.now(timezone.utc),
        )
    ]

    def fake_find_regions_intersecting_point(db, latitude, longitude):
        return expected_regions

    monkeypatch.setattr(region_service, "find_regions_intersecting_point", fake_find_regions_intersecting_point)

    response = client.post("/intersects", json={"latitude": 30.0, "longitude": 31.0})

    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]["name"] == "Cairo"


def test_intersects_service_delegates_to_repository() -> None:
    db = MagicMock()
    expected_regions = [MagicMock()]

    def fake_find_intersecting_regions(db_arg, latitude, longitude):
        assert db_arg is db
        assert latitude == 30.0
        assert longitude == 31.0
        return expected_regions

    original = region_repository.find_intersecting_regions
    region_repository.find_intersecting_regions = fake_find_intersecting_regions
    try:
        regions = region_service.find_regions_intersecting_point(db, 30.0, 31.0)
    finally:
        region_repository.find_intersecting_regions = original

    assert regions == expected_regions


def test_intersects_repository_uses_st_intersects() -> None:
    db = MagicMock()
    db.execute.return_value.scalars.return_value.all.return_value = []

    region_repository.find_intersecting_regions(db, 30.0, 31.0)

    statement = db.execute.call_args.args[0]
    assert "ST_Intersects" in str(statement)