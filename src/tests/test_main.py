import httpx

from fastapi.testclient import TestClient
from httpx import WSGITransport

from main import app

client = TestClient(app)
# client = httpx.Client(transport=WSGITransport(app=app))


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
