import json
import pytest
from fastapi.testclient import TestClient
from src.streaming.schemas import Track, TrackCreate, TrackUpdate, TrackResponse
from src.main import app
from src.streaming.models import Track as TrackModel

client = TestClient(app)


@pytest.fixture(scope="module")
def track():
    return TrackCreate(
        title="Test Track",
        author="Test Author",
        genre="Test Genre",
        date="2022-05-01",
        link_to_file="https://test.com/test.mp3",
    )


def test_create_track(track):
    response = client.post("/tracks", json=track.dict())
    assert response.status_code == 200
    created_track = Track(**response.json())
    assert created_track.id is not None
    assert created_track.title == track.title
    assert created_track.author == track.author
    assert created_track.genre == track.genre
    assert str(created_track.date) == track.date
    assert created_track.link_to_file == track.link_to_file


def test_get_track_by_id(track):
    # Create the track
    response = client.post("/tracks", json=track.dict())
    created_track = Track(**response.json())

    # Retrieve the track by ID
    response = client.get(f"/tracks/{created_track.id}")
    assert response.status_code == 200
    retrieved_track = Track(**response.json())
    assert created_track.dict() == retrieved_track.dict()


def test_get_tracks_by_musician(track):
    # Create the track
    response = client.post("/tracks", json=track.dict())
    created_track = Track(**response.json())

    # Retrieve the track by musician
    response = client.get(f"/tracks/search?musician={created_track.author}")
    assert response.status_code == 200
    retrieved_tracks = [Track(**item) for item in response.json()]
    assert len(retrieved_tracks) == 1
    assert created_track.dict() == retrieved_tracks[0].dict()


def test_get_tracks_by_title(track):
    # Create the track
    response = client.post("/tracks", json=track.dict())
    created_track = Track(**response.json())

    # Retrieve the track by title
    response = client.get(f"/tracks/search?track={created_track.title}")
    assert response.status_code == 200
    retrieved_tracks = [Track(**item) for item in response.json()]
    assert len(retrieved_tracks) == 1
    assert created_track.dict() == retrieved_tracks[0].dict()


def test_get_tracks_by_query(track):
    # Create the track
    response = client.post("/tracks", json=track.dict())
    created_track = Track(**response.json())

    # Retrieve the track by query
    response = client.get(f"/tracks/search?query={created_track.title}")
    assert response.status_code == 200
    retrieved_tracks = [Track(**item) for item in response.json()]
    assert len(retrieved_tracks) == 1
    assert created_track.dict() == retrieved_tracks[0].dict()


def test_update_track(track):
    # Create the track
    response = client.post("/tracks", json=track.dict())
    created_track = Track(**response.json())

    # Update the track
    updated_track = TrackUpdate(
        id=created_track.id,
        title="Updated Track",
        author="Updated Author",
        genre="Updated Genre",
        date="2022-05-02",
        link_to_file="https://test.com/updated.mp3",
    )
    response = client.put(f"/tracks/{created_track.id}", json=updated_track.dict())
    assert response.status_code == 200

