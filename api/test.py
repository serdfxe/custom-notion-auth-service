import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from api.auth import auth_router
from api.user import user_router
from api.auth.generate_token import JWTService


app = FastAPI()
app.include_router(auth_router)
app.include_router(user_router)


@pytest.fixture(scope="module")
def client():
    app = FastAPI()
    app.include_router(auth_router)
    app.include_router(user_router)
    return TestClient(app)


@pytest.fixture
def created_user(client):
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "newpassword",
    }
    response = client.post("/user/", json=user_data)

    assert response.status_code == 200
    return response.json()


# Тест для получения токена
def test_get_token_route(client):
    test_email = "testuser@example.com"
    test_password = "testpassword"
    user_data = {"username": "testuser", "email": test_email, "password": test_password}
    response = client.post("/user/", json=user_data)

    assert response.status_code == 200

    response = client.post(
        "/auth/token", json={"email": test_email, "password": test_password}
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


# Тест для проверки токена
def test_verify_token_route(client):
    jwt_service = JWTService()
    token = jwt_service.encode_jwt({"sub": "testuser"})

    response = client.get("/auth/verify", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == {"message": "Token is valid."}


# Тест для проверки неверного токена
def test_verify_invalid_token_route(client):
    response = client.get(
        "/auth/verify", headers={"Authorization": "Bearer invalidtoken"}
    )

    assert response.status_code == 401
    error_message = response.json().get("detail", "")
    assert "Invalid or expired token" in error_message


# Тест для создания пользователя
def test_create_user_route(client):
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "newpassword",
    }

    response = client.post("/user/", json=user_data)

    assert response.status_code == 200
    assert "username" in response.json()
    assert response.json()["username"] == user_data["username"]


# Тест для получения данных пользователя с неверным токеном
def test_get_user_invalid_token_route(client):
    response = client.get("/user/", headers={"Authorization": "Bearer invalidtoken"})

    assert response.status_code == 401
    response_json = response.json()
    detail = response_json.get("detail")
    assert detail["error_message"] == "Invalid or expired token"
    assert detail["error_code"] == 6


# Тест для удаления пользователя с неверным токеном
def test_delete_user_invalid_token_route(client):
    response = client.delete("/user/", headers={"Authorization": "Bearer invalidtoken"})

    assert response.status_code == 400
    response_json = response.json()
    detail = response_json.get("detail")
    assert detail["error_massage"] == "Invalid or expired token"
    assert detail["error_code"] == 3
