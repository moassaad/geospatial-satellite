from fastapi import status

VALID_GEOMETRY = {
    "type": "Polygon",
    "coordinates": [
        [
            [31.0, 30.0],
            [31.5, 30.0],
            [31.5, 30.5],
            [31.0, 30.5],
            [31.0, 30.0],
        ]
    ],
}

INVALID_GEOMETRY = {
    "type": "Polygon",
    "coordinates": [
        [
            [0.0, 0.0],
            [2.0, 2.0],
            [2.0, 0.0],
            [0.0, 2.0],
            [0.0, 0.0],
        ]
    ],
}


class TestCreateRegion:
    def test_creates_region(self, client) -> None:
        response = client.post("/regions", json={"name": "Cairo", "geometry": VALID_GEOMETRY})
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == "Cairo"
        assert data["geometry"]["type"] == "Polygon"
        assert data["id"] > 0
        assert "created_at" in data

    def test_rejects_invalid_geometry(self, client) -> None:
        response = client.post(
            "/regions",
            json={"name": "Broken", "geometry": INVALID_GEOMETRY},
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestListRegions:
    def test_lists_regions(self, client) -> None:
        client.post("/regions", json={"name": "Cairo", "geometry": VALID_GEOMETRY})
        response = client.get("/regions")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert any(region["name"] == "Cairo" for region in data)


class TestReadRegion:
    def test_gets_region_by_id(self, client) -> None:
        created = client.post("/regions", json={"name": "Cairo", "geometry": VALID_GEOMETRY}).json()
        response = client.get(f"/regions/{created['id']}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == "Cairo"

    def test_returns_not_found_for_missing_region(self, client) -> None:
        response = client.get("/regions/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateRegion:
    def test_updates_region_name(self, client) -> None:
        created = client.post("/regions", json={"name": "Cairo", "geometry": VALID_GEOMETRY}).json()
        response = client.put(f"/regions/{created['id']}", json={"name": "Giza"})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == "Giza"

    def test_returns_not_found_for_missing_region(self, client) -> None:
        response = client.put("/regions/99999", json={"name": "Giza"})
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteRegion:
    def test_deletes_region(self, client) -> None:
        created = client.post("/regions", json={"name": "Cairo", "geometry": VALID_GEOMETRY}).json()
        response = client.delete(f"/regions/{created['id']}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_returns_not_found_for_missing_region(self, client) -> None:
        response = client.delete("/regions/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND