import pytest
from fastapi.testclient import TestClient
from app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Бэкенд для курсового проекта. Для документации вызовите /docs"


def test_ping(client):
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}


def test_docs(client):
    response = client.get("/docs")
    assert response.status_code == 200


def test_json(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
