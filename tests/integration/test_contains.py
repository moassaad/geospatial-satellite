from fastapi import status

REGION_PAYLOAD = {
    "name": "Cairo",
    "geometry": {
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
    },
}


class TestContainsEndpoint:
    def _seed_region(self, client) -> None:
        created = client.post("/regions", json=REGION_PAYLOAD)
        assert created.status_code == status.HTTP_201_CREATED

    def test_returns_region_containing_point(self, client) -> None:
        self._seed_region(client)
        response = client.post("/contains", json={"latitude": 30.2, "longitude": 31.2})
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert any(region["name"] == "Cairo" for region in data)

    def test_returns_empty_when_point_is_outside(self, client) -> None:
        self._seed_region(client)
        response = client.post("/contains", json={"latitude": 35.0, "longitude": 35.0})
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []