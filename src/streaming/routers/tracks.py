from fastapi import APIRouter
from src.streaming.schemas import Track, TrackCreate, TrackUpdate, TrackResponse
from src.streaming.models import Track as TrackModel
from src.database import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

router = APIRouter()


def create_track(track: TrackCreate):
    with Session() as session:
        db_track = TrackModel(**track.dict())

        try:
            session.commit(db_track)
            session.refresh(db_track)
            return db_track
        except SQLAlchemyError as e:
            session.rollback()
            raise HTTPException(status_code=500, detail="Database Error: " + str(e))
    return db_track


def get_track(track_id: int):
    with Session() as session:
        db_tracks = session.query(TrackModel).filter(TrackModel.id == track_id).first()
        if db_tracks is None:
            raise HTTPException(status_code=404, detail="Track not found")
        return db_tracks


def get_by_musician(musician: str):
    with Session() as session:
        db_tracks = session.query(TrackModel).filter(TrackModel.author == musician).first()
        if db_tracks is None:
            raise HTTPException(status_code=404, detail="Track not found")
        return db_tracks


def get_by_tittle(tittle: str):
    with Session() as session:
        db_tracks = session.query(TrackModel).filter(TrackModel.tittle == tittle).first()
        if db_tracks is None:
            raise HTTPException(status_code=404, detail="Track not found")
        return db_tracks


def get_many_tracks():
    with Session() as session:
        db_tracks = session.query(TrackModel).all()
        return db_tracks


def update_track(track_id: int, track: TrackModel):
    with Session() as session:
        db_track = session.query(TrackModel).filter(TrackModel.id == track_id).first()
        if db_track is None:
            raise HTTPException(status_code=404, detail="Track not found")
        for field, value in track:
            setattr(db_track, field, value)
        try:
            session.commit()
            session.refresh(db_track)
            return db_track
        except  SQLAlchemyError as e:
            session.rollback()
            raise HTTPException(status_code=500, detail="Database Error: " + str(e))


def delete_track(track_id: int):
    with Session() as session:
        db_track = session.query(TrackModel).filter(TrackModel.id == track_id).first()
        if db_track is None:
            raise HTTPException(status_code=404, detail="Track not found")
        try:
            session.delete(db_track)
            session.commit()
        except  SQLAlchemyError as e:
            session.rollback()
            raise HTTPException(status_code=500, detail="Database Error: " + str(e))


@router.get("/tracks")
async def get_tracks():
    return get_many_tracks()


@router.get("/tracks/{id}")
async def get_track_by_id(track_id: id):
    return get_track(track_id)


@router.get("/tracks/search?musician={musician}")
async def get_tracks_by_musician(musician: str):
    return get_by_musician(musician)


@router.get("/tracks/search?track={track_tittle}")
async def get_tracks_by_tittle(track_tittle: str):
    return get_by_tittle(track_tittle)


@router.get("/tracks/search?query={query}")
async def get_tracks_by_query(query: str):
    with Session() as session:
        db_track = session.query(TrackModel).filter(TrackModel.title.ilike(f"%{query}%")).all()
        if db_track is None:
            raise HTTPException(status_code=404, detail="Track not found")
        return db_track


@router.post("/tracks")
async def сreate_track_by_id(track: TrackCreate):
    return create_track(track)


@router.put("/tracks/{track_id}")
async def update_new_track(track_id: int, track: TrackModel):
    return update_track(track_id, track)


@router.delete("/tracks/{track_id}")
async def delete_track(track_id: int):
    return delete_track(track_id)
