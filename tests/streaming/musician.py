from fastapi.testclient import TestClient
from src.database import SessionLocal
from src.main import app
from src.streaming.schemas import MusicianUpdate
from src.streaming.models import Musician
from datetime import date

client = TestClient(app)


# Test musician CRUD endpoints
def test_create_musician():
    # create a test musician
    musician = {"name": "John Lennon"}

    # make a request to create the musician
    response = client.post("/musicians", json=musician)

    # check that the response is successful and returns the created musician
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "John Lennon","genre":'country'}


def test_get_musician():
    # create a test musician
    musician = {'id':1,"name": "John Lennon","genre":'country'}
    session = SessionLocal()
    db_musician = Musician(**musician.dict())
    session.add(db_musician)
    session.commit()
    session.refresh(db_musician)

    # make a request to retrieve the musician by id
    response = client.get(f"/musicians/{db_musician.id}")

    # check that the response is successful and returns the musician
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "John Lennon","genre":'country'}


def test_get_musician_by_title():
    # create a test musician
    musician = {"name": "John Lennon"}
    session = SessionLocal()
    db_musician = Musician(**musician.dict())
    session.add(db_musician)
    session.commit()
    session.refresh(db_musician)

    # make a request to retrieve the musician by title
    response = client.get(f"/musicians/search?musician={db_musician.name}")

    # check that the response is successful and returns the musician
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "John Lennon","genre":'country'}]


def test_get_many_musicians():
    # create some test musicians
    musicians = [
        {"name": "John Lennon","genre":'country'},
        {"name": "Paul McCartney","genre":'country'},
        {"name": "George Harrison","genre":'country'},
        {"name": "Ringo Starr","genre":'country'}
    ]
    session = SessionLocal()
    for musician in musicians:
        db_musician = Musician(**musician.dict())
        session.add(db_musician)
        session.commit()
        session.refresh(db_musician)

    # make a request to retrieve all musicians
    response = client.get("/musicians")

    # check that the response is successful and returns all the musicians
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "John Lennon","genre":'country'},
        {"id": 2, "name": "Paul McCartney","genre":'country'},
        {"id": 3, "name": "George Harrison","genre":'country'},
        {"id": 4, "name": "Ringo Starr","genre":'country'}
    ]


def test_update_musician(musician):
    # Create the track
    response = client.post("/musicians", json=musician.dict())
    created_musician = Musician(**response.json())

    # Update the track
    updated_musician = MusicianUpdate(
        id='1',
        name='Johny Lenons',
        genre='country',
        year_start='1754',
        year_end='2023',

    )
    response = client.put(f"/musician/{created_musician.id}", json=updated_musician.dict())
    assert response.status_code == 200
