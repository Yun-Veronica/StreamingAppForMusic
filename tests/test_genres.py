from fastapi.testclient import TestClient
from src.main import app
from src.streaming.schemas import GenreCreate

test_client = TestClient(app)


def test_create_genre():
    genre_data = {"title": "Rock"}
    response = test_client.post("/genres", json=genre_data)
    assert response.status_code == 200
    assert response.json()["title"] == genre_data["title"]


def test_get_genre():
    genre_data = {"title": "Jazz"}
    genre_create_response = test_client.post("/genres", json=genre_data).json()
    genre_id = genre_create_response["id"]
    response = test_client.get(f"/genres/{genre_id}")
    assert response.status_code == 200
    assert response.json()["title"] == genre_data["title"]


def test_get_many_genres():
    genre_data = {"title": "Classical"}
    genre_create_response = test_client.post("/genres", json=genre_data).json()
    response = test_client.get("/genres")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_update_genre():
    genre_data = {"title": "Pop"}
    genre_create_response = test_client.post("/genres", json=genre_data).json()
    genre_id = genre_create_response["id"]
    updated_genre_data = {"title": "New Pop"}
    response = test_client.put(f"/genres/{genre_id}", json=updated_genre_data)
    assert response.status_code == 200
    assert response.json()["title"] == updated_genre_data["title"]


def test_delete_genre():
    genre_data = {"title": "Metal"}
    genre_create_response = test_client.post("/genres", json=genre_data).json()
    genre_id = genre_create_response["id"]
    response = test_client.delete(f"/genres/{genre_id}")
    assert response.status_code == 200
    assert response.json() == None
