# crud for genres
from fastapi import APIRouter
from src.streaming.schemas import GenreUpdate,GenreResponse,GenreCreate, Genre
from src.streaming.models import Genre as GenreModel
from src.database import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from typing import List

router = APIRouter()



def create_genre(genre: GenreCreate):
    with Session() as session:
        db_genre = GenreModel(**genre.dict())

        try:
            session.commit(db_genre)
            session.refresh(db_genre)
            return db_genre
        except SQLAlchemyError as e:
            session.rollback()
            raise HTTPException(status_code=500, detail="Database Error: " + str(e))
    return db_genre


def get_genre(genre_id: int):
    with Session() as session:
        db_genre = session.query(GenreModel).filter(GenreModel.id == genre_id).first()
        if db_genre is None:
            raise HTTPException(status_code=404, detail="Genre not found")
        return db_genre



def get_many_genres():
    with Session() as session:
        db_genre = session.query(GenreModel).all()
        return db_genre


def update_genre(genre_id: int, genre: GenreModel):
    with Session() as session:
        db_genre = session.query(GenreModel).filter(GenreModel.id == genre_id).first()
        if db_genre is None:
            raise HTTPException(status_code=404, detail="Genre not found")
        for field, value in genre:
            setattr(db_genre, field, value)
        try:
            session.commit()
            session.refresh(db_genre)
            return db_genre
        except  SQLAlchemyError as e:
            session.rollback()
            raise HTTPException(status_code=500, detail="Database Error: " + str(e))


def delete_genre(genre_id: int):
    with Session() as session:
        db_genre = session.query(GenreModel).filter(GenreModel.id == genre_id).first()
        if db_genre is None:
            raise HTTPException(status_code=404, detail="Genre not found")
        try:
            session.delete(db_genre)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise HTTPException(status_code=500, detail="Database Error: " + str(e))


@router.get("/genres")
async def get_genres()-> List[Genre]:
    return get_many_genres()


@router.get("/genres/{id}")
async def get_genre_by_id(genre_id: id)->Genre:
    return get_genre(genre_id)




@router.post("/genres")
async def create_genre(genre: GenreCreate)->Genre:
    return create_genre(genre)


@router.put("/genres/{genre_id}")
async def update_genre(genre_id: int, genre: Genre)->Genre:
    return update_genre(genre_id, genre)


@router.delete("/genres/{genre_id}")
async def delete_genre(genre_id: int):
    return delete_genre(genre_id)
