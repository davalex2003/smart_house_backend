import pytest
from fastapi.testclient import TestClient
from app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_validate_new_email(client):
    response = client.post("/users/validate_email", json={"e_mail": "pupkinvasek200356@gmail.com"})
    assert response.status_code == 200


def test_validate_existing_email(client):
    response = client.post("/users/validate_email", json={"e_mail": "davalex2003@yandex.ru"})
    assert response.status_code == 400
    assert response.json() == {"message": "Email already used"}


def test_register(client):
    response = client.post("/users/register", json={
        "name": "Алексей",
        "surname": "Давиденко",
        "e_mail": "pupkinvasek200356@gmail.com",
        "hash_password": "password"
    })
    assert response.status_code == 201
    assert 'token' in response.json()


def test_authorize(client):
    response = client.post("/users/authorize", json={
        "e_mail": "davalex2003@yandex.ru",
        "hash_password": "password"
    })
    assert response.status_code == 200
    assert 'token' in response.json()


def test_authorize_fail(client):
    response = client.post("/users/authorize", json={
        "e_mail": "davalex2003@yandex.ru",
        "hash_password": "passwords"
    })
    assert response.status_code == 401


def test_info(client):
    response = client.post("/users/authorize", json={
        "e_mail": "pupkinvasek200356@gmail.com",
        "hash_password": "password"
    })
    token = response.json()['token']
    response = client.get("/users/info", headers={"Authorization": f"{token}"})
    assert response.status_code == 200
    assert response.json() == {
        "name": "Алексей",
        "surname": "Давиденко"
    }


def test_update(client):
    response = client.post("/users/authorize", json={
        "e_mail": "pupkinvasek200356@gmail.com",
        "hash_password": "password"
    })
    token = response.json()['token']
    response = client.put("/users/update", json={
        "name": "Максим",
        "surname": "Давиденко"
    }, headers={"Authorization": f"{token}"})
    assert response.status_code == 200
    assert response.json() == {"message": "Updated"}
    response = client.get("/users/info", headers={"Authorization": f"{token}"})
    assert response.status_code == 200
    assert response.json() == {
        "name": "Максим",
        "surname": "Давиденко"
    }


def test_delete_without_token(client):
    response = client.delete("/users/delete")
    assert response.status_code == 401
    assert response.json() == {"message": "Not found token"}


def test_delete_with_bad_token(client):
    response = client.post("/users/authorize", json={
        "e_mail": "pupkinvasek200356@gmail.com",
        "hash_password": "password"
    })
    token = response.json()['token']
    response = client.delete("/users/delete", headers={"Authorization": f"{token[::-1]}"})
    assert response.status_code == 401
    assert response.json() == {"message": "Wrong token"}


def test_delete(client):
    response = client.post("/users/authorize", json={
        "e_mail": "pupkinvasek200356@gmail.com",
        "hash_password": "password"
    })
    token = response.json()['token']
    response = client.delete("/users/delete", headers={"Authorization": f"{token}"})
    assert response.status_code == 200
