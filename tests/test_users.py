import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import timedelta
from fastapi.testclient import TestClient

from src.main import app
from src.auth.token_config import ACCESS_TOKEN_EXPIRE_MINUTES
from src.auth.auth_scripts import create_access_token
from src.database import SQLALCHEMY_DATABASE_URL


engine = create_engine(SQLALCHEMY_DATABASE_URL)
client = TestClient(app)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_testing_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# @pytest.fixture(scope="module")
# def client():
#     app.dependency_overrides[get_testing_db] = get_testing_db
#     client = TestClient(app)
#     yield client


def test_create_user(client):
    new_user = {
        "email": "test@example.com",
        "full_name": "Test User",
        "username": "testuser",
        "password": "password123"
    }
    response = client.post("/register/", json=new_user)
    assert response.status_code == 200
    assert response.json()["username"] == new_user["username"]


def test_create_user_duplicate_email(client):
    new_user = {
        "email": "test@example.com",
        "full_name": "Test User",
        "username": "testuser",
        "password": "password123"
    }
    client.post("/register/", json=new_user)
    response = client.post("/register/", json=new_user)
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_create_access_token(client):
    new_user = {
        "email": "test@example.com",
        "full_name": "Test User",
        "username": "testuser",
        "password": "password123"
    }
    client.post("/register/", json=new_user)
    response = client.post(
        "/token",
        data={"grant_type": "password", "username": new_user["email"], "password": new_user["password"]}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_create_access_token_invalid_credentials(client):
    new_user = {
        "email": "test@example.com",
        "full_name": "Test User",
        "username": "testuser",
        "password": "password123"
    }
    client.post("/register/", json=new_user)
    response = client.post(
        "/token",
        data={"grant_type": "password", "username": new_user["email"], "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "detail" in response.json()
    assert "Could not validate credentials" in response.json()["detail"]


def test_create_access_token_expired(client):
    new_user = {
        "email": "test@example.com",
        "full_name": "Test User",
        "username": "testuser",
        "password": "password123"
    }
    client.post("/register/", json=new_user)
    access_token_expires = timedelta(minutes=0)
    access_token = create_access_token(data={"sub": new_user["email"]}, expires_delta=access_token_expires)
    response = client.get("/users/me/", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 401
    assert "detail" in response.json()


def test_registration():
    response = client.post(
        "/register/",
        json={
            "email": "test_user@example.com",
            "full_name": "Test User",
            "password": "test_password",
        },
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test_user@example.com"


def test_registration_duplicate_email():
    response = client.post(
        "/register/",
        json={
            "email": "test_user@example.com",
            "full_name": "Test User",
            "password": "test_password",
        },
    )
    assert response.status_code == 400


def test_login():
    response = client.post(
        "/token",
        data={
            "grant_type": "password",
            "username": "test_user@example.com",
            "password": "test_password",
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_incorrect_password():
    response = client.post(
        "/token",
        data={
            "grant_type": "password",
            "username": "test_user@example.com",
            "password": "wrong_password",
        },
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_get_user():
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": "test_user@example.com"}, expires_delta=access_token_expires
    )
    response = client.get("/users/test_user@example.com", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "test_user@example.com"


def test_get_user_not_authenticated():
    response = client.get("/users/test_user@example.com")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_get_user_inactive():
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": "test_user@example.com", "disabled": True},
        expires_delta=access_token_expires,
    )
    response = client.get("/users/test_user@example.com", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Inactive user"
