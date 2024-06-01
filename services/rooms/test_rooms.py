import pytest
from fastapi.testclient import TestClient
from app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_rooms(client):
    response = client.post("/users/register", json={
        "name": "Алексей",
        "surname": "Давиденко",
        "e_mail": "pupkinvasek200356@gmail.com",
        "hash_password": "password"
    })
    token = response.json()['token']
    response = client.post("/rooms/create", json={"name": "Кухня"}, headers={"Authorization": f"{token}"})
    assert response.status_code == 201
    assert "id" in response.json()
    room_id = response.json()['id']
    response = client.get("/rooms/list", headers={"Authorization": f"{token}"})
    assert response.status_code == 200
    assert response.json()[0]['name'] == 'Кухня'
    response = client.put("/rooms/update", json={"id": room_id, "name": "Зал"}, headers={"Authorization": f"{token}"})
    assert response.status_code == 200
    response = client.get("/rooms/list", headers={"Authorization": f"{token}"})
    assert response.status_code == 200
    assert response.json()[0]['name'] == 'Зал'
    response = client.get("/rooms/devices", params={"room_id": room_id}, headers={"Authorization": f"{token}"})
    assert response.status_code == 200
    response = client.delete("/rooms/delete", headers={"Authorization": f"{token}"}, params={"room_id": room_id})
    assert response.status_code == 200
    client.delete("/users/delete", headers={"Authorization": f"{token}"})
