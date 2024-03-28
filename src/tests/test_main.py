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


def test_get_todos(mocker):

    mocker.patch(
        "main.get_todos",
        return_value=[
            {"id": 1, "contents": "buy milk", "is_done": True},
            {"id": 2, "contents": "buy bread", "is_done": True},
            {"id": 3, "contents": "buy egg", "is_done": True},
        ],
    )

    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == {
        "todos": [
            {"id": 1, "contents": "buy milk", "is_done": True},
            {"id": 2, "contents": "buy bread", "is_done": True},
            {"id": 3, "contents": "buy egg", "is_done": True},
        ]
    }

    response = client.get("/todos?order=DESC")
    assert response.status_code == 200
    assert response.json() == {
        "todos": [
            {"id": 3, "contents": "buy egg", "is_done": True},
            {"id": 2, "contents": "buy bread", "is_done": True},
            {"id": 1, "contents": "buy milk", "is_done": True},
        ]
    }
