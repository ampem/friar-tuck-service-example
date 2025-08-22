import pytest
from fastapi.testclient import TestClient
from app.handler_http import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.asyncio
async def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "OK"}


@pytest.mark.asyncio
async def test_fail_endpoint(client):
    response = client.get("/fail")
    assert response.status_code == 400
    assert response.json() == {"message": "Failure"}
