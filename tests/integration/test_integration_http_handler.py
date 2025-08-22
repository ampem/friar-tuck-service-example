import pytest
from fastapi.testclient import TestClient
from app.handler_http import app

@pytest.mark.integration
class TestHttpHandlerIntegration:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    @pytest.mark.asyncio
    async def test_root_endpoint(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "OK"}

    @pytest.mark.asyncio
    async def test_fail_endpoint(self, client):
        response = client.get("/fail")
        assert response.status_code == 400
        assert response.json() == {"message": "Failure"}

    @pytest.mark.asyncio
    async def test_info_endpoint(self, client):
        response = client.get("/info")
        assert response.status_code == 200
        assert response.json() == {"info": "service-example"}
