# crud for musician
from fastapi import APIRouter
from src.streaming.schemas import Musician, MusicianUpdate, MusicianResponse, MusicianCreate
from src.streaming.models import Musician as MusicianModel
from src.streaming.models import Genre
from src.database import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from sqlalchemy.orm import joinedload

router = APIRouter()


def create_musician(musician: MusicianCreate, session):
    with session:
        musician_dict = musician.dict()
        db_musician = MusicianModel(id=musician_dict['id'],
                                    name=musician_dict['name'],
                                    year_start=musician_dict['year_start'],
                                    genre_id=musician_dict['genre_id'],
                                    year_end=musician_dict['year_end']
                                    )

        try:
            session.add(db_musician)
            session.commit()
            session.refresh(db_musician)
            return db_musician
        except SQLAlchemyError as e:
            session.rollback()
            raise HTTPException(status_code=500, detail="Database Error: " + str(e))
    return db_musician


def get_musician(musician_id: int, session):
    with session:
        db_musician = session.query(MusicianModel).filter(MusicianModel.id == musician_id).first()
        if db_musician is None:
            raise HTTPException(status_code=404, detail="Musician not found")
        return db_musician


def get_by_tittle(tittle: str, session):
    with session:
        db_musician = session.query(MusicianModel).filter(MusicianModel.name.like(f'%{tittle}%')).first()
        if db_musician is None:
            raise HTTPException(status_code=404, detail="Musician not found")
        return db_musician


def get_many_musicians(session):
    with session:
        # db_musician = session.query(MusicianModel).all()
        db_musician = session.query(MusicianModel).all()
        return db_musician


def update_musician(musician_id: int, musician: MusicianModel, session):
    with session:
        db_musician = session.query(MusicianModel).filter(MusicianModel.id == musician_id).first()
        if db_musician is None:
            raise HTTPException(status_code=404, detail="Musician not found")
        for field, value in musician:
            setattr(db_musician, field, value)
        try:
            session.add(db_musician)
            session.commit()
            session.refresh(db_musician)
            return db_musician
        except  SQLAlchemyError as e:
            session.rollback()
            raise HTTPException(status_code=500, detail="Database Error: " + str(e))


def delete_musician(musician_id: int, session):
    with session:
        db_musician = session.query(MusicianModel).filter(MusicianModel.id == musician_id).first()
        if db_musician is None:
            raise HTTPException(status_code=404, detail="Musician not found")
        try:
            session.delete(db_musician)
            session.commit()
        except  SQLAlchemyError as e:
            session.rollback()
            raise HTTPException(status_code=500, detail="Database Error: " + str(e))


@router.get("/musicians")
async def get_musicians() -> list:
    with Session() as session:
        return get_many_musicians(session)


@router.get("/musicians/{id}")
async def get_musician_by_id(musician_id: int) -> Musician:
    with Session() as session:
        return get_musician(musician_id, session)


@router.get("/musicians/search?musician={musician_tittle}")
async def get_musicians_by_tittle(musician_tittle: str) -> list:
    with Session() as session:
        return get_by_tittle(musician_tittle, session)


@router.post("/musicians")
async def create_musician_(musician: MusicianCreate) -> Musician:
    with Session() as session:
        return create_musician(musician, session)


@router.put("/musicians/{musician_id}")
async def update_new_musician(musician_id: int, musician: Musician) -> Musician:
    with Session() as session:
        return update_musician(musician_id, musician, session)


@router.delete("/musicians/{musician_id}")
async def delete_musician_(musician_id: int):
    with Session() as session:
        return delete_musician(musician_id, session)
