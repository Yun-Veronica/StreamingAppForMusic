from fastapi import APIRouter
from src.streaming.schemas import Track, TrackCreate, TrackUpdate, TrackResponse
from src.streaming.models import Track as TrackModel
from src.database import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

router = APIRouter()


def create_track(track: TrackCreate,session):
    with  session:
        db_track = TrackModel(**dict(track))
        try:
            session.add(db_track)
            session.commit()
            session.refresh(db_track)
            return db_track
        except SQLAlchemyError as e:
            session.rollback()
            raise HTTPException(status_code=500, detail="Database Error: " + str(e))
    return db_track


def get_track(track_id: int,session):
    with session:
        db_tracks = session.query(TrackModel).filter(TrackModel.id == track_id).first()
        if db_tracks is None:
            raise HTTPException(status_code=404, detail="Track not found")
        return db_tracks


def get_by_musician(musician: str,session):
    with  session:
        db_tracks = session.query(TrackModel).filter(TrackModel.author == musician).first()
        if db_tracks is None:
            raise HTTPException(status_code=404, detail="Track not found")
        return db_tracks


def get_by_tittle(tittle: str,session):
    with session:
        db_tracks = session.query(TrackModel).filter(TrackModel.tittle.like(f'%{tittle}%')).all()
        if db_tracks is None:
            raise HTTPException(status_code=404, detail="Track not found")
        return db_tracks


def get_many_tracks(session):
    with session:
        db_tracks = session.query(TrackModel).all()
        return db_tracks


def update_track(track_id: int, track: TrackModel, session):
    with session:
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


def delete_track(track_id: int, session):
    with session:
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
async def get_tracks()->list:
    with Session() as session:
        return get_many_tracks(session)


@router.get("/tracks/{id}")
async def get_track_by_id(track_id: int)->Track:
    with Session() as session:
        return get_track(track_id,session)


@router.get("/tracks/search?track={track_tittle}")
async def get_tracks_by_tittle(track_tittle: str)->list:
    with Session() as session:
        return get_by_tittle(track_tittle,session)


@router.get("/tracks/search?query={query}")
async def get_tracks_by_query(query: str)->Track:
    with Session() as session:
        db_track = session.query(TrackModel).filter(TrackModel.title.ilike(f"%{query}%")).all()
        if db_track is None:
            raise HTTPException(status_code=404, detail="Track not found")
        return db_track


@router.post("/tracks")
async def сreate_track_by_id(track: TrackCreate)->Track:
    with Session() as session:
        return create_track(track,session)


@router.put("/tracks/{track_id}")
async def update_new_track(track_id: int, track: Track)->Track:
    with Session() as session:
        return update_track(track_id, track,session)


@router.delete("/tracks/{track_id}")
async def delete_track_(track_id: int):
    with Session() as session:
        return delete_track(track_id,session)
