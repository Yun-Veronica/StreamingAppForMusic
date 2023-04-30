from fastapi.testclient import TestClient
from src.main import app
from src.streaming.models import Playlist

client = TestClient(app)

def test_create_playlist():
    playlist = {"title": "New Playlist", "description": "A new playlist", "user_id": 1}
    response = client.post("/playlists", json=playlist)
    assert response.status_code == 200
    assert response.json()["title"] == playlist["title"]
    assert response.json()["description"] == playlist["description"]
    assert response.json()["user_id"] == playlist["user_id"]

def test_get_playlist():
    playlist_id = 1
    response = client.get(f"/playlists/{playlist_id}")
    assert response.status_code == 200
    assert response.json()["id"] == playlist_id

def test_get_nonexistent_playlist():
    playlist_id = 999
    response = client.get(f"/playlists/{playlist_id}")
    assert response.status_code == 404

def test_update_playlist():
    playlist_id = 1
    new_playlist = {"title": "Updated Playlist", "description": "An updated playlist"}
    response = client.put(f"/playlists/{playlist_id}", json=new_playlist)
    assert response.status_code == 200
    assert response.json()["title"] == new_playlist["title"]
    assert response.json()["description"] == new_playlist["description"]

def test_delete_playlist():
    playlist_id = 1
    response = client.delete(f"/playlists/{playlist_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Playlist deleted successfully"}

def test_get_playlists():
    response = client.get("/playlists")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for playlist in response.json():
        assert isinstance(playlist, Playlist)
