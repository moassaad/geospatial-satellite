from fastapi import status


class TestHealthEndpoint:
    def test_reports_healthy_database(self, client) -> None:
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
        body = response.json()
        assert body["status"] == "ok"
        assert body["database"]["status"] == "ok"