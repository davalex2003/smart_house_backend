import pytest
from fastapi.testclient import TestClient
from app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_devices(client):
    response = client.post("/users/register", json={
        "name": "Алексей",
        "surname": "Давиденко",
        "e_mail": "pupkinvasek200356@gmail.com",
        "hash_password": "password"
    })
    token = response.json()['token']
    response = client.post("/rooms/create", json={"name": "Спальня"}, headers={"Authorization": f"{token}"})
    assert response.status_code == 201
    assert "id" in response.json()
    room_id = response.json()['id']
    response = client.post("/devices/create", json={
        "room_id": room_id,
        "name": "Марина",
        "type": "clock",
        "ip": "localhost"
    }, headers={"Authorization": f"{token}"})
    assert response.status_code == 201
    assert "id" in response.json()
    device_id = response.json()['id']
    response = client.delete("/devices/delete", headers={"Authorization": f"{token}"}, params={"device_id": device_id})
    assert response.status_code == 200
    client.delete("/users/delete", headers={"Authorization": f"{token}"})
    assert response.status_code == 200
