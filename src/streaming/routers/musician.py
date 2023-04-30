# crud for musician
from fastapi import APIRouter
from src.streaming.schemas import Musician, MusicianUpdate, MusicianResponse, MusicianCreate
from src.streaming.models import Musician as MusicianModel
from src.database import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

router = APIRouter()

def create_musician(musician: MusicianCreate):
    with Session() as session:
        db_musician = MusicianModel(**musician.dict())

        try:
            session.commit(db_musician)
            session.refresh(db_musician)
            return db_musician
        except SQLAlchemyError as e:
            session.rollback()
            raise HTTPException(status_code=500, detail="Database Error: " + str(e))
    return db_musician


def get_musician(musician_id: int):
    with Session() as session:
        db_musician = session.query(MusicianModel).filter(MusicianModel.id == musician_id).first()
        if db_musician is None:
            raise HTTPException(status_code=404, detail="Musician not found")
        return db_musician



def get_by_tittle(tittle: str):
    with Session() as session:
        db_musician = session.query(MusicianModel).filter(MusicianModel.tittle == tittle).first()
        if db_musician is None:
            raise HTTPException(status_code=404, detail="Musician not found")
        return db_musician


def get_many_musicians():
    with Session() as session:
        db_musician = session.query(MusicianModel).all()
        return db_musician


def update_musician(musician_id: int, musician: MusicianModel):
    with Session() as session:
        db_musician = session.query(MusicianModel).filter(MusicianModel.id == musician_id).first()
        if db_musician is None:
            raise HTTPException(status_code=404, detail="Musician not found")
        for field, value in musician:
            setattr(db_musician, field, value)
        try:
            session.commit()
            session.refresh(db_musician)
            return db_musician
        except  SQLAlchemyError as e:
            session.rollback()
            raise HTTPException(status_code=500, detail="Database Error: " + str(e))


def delete_musician(musician_id: int):
    with Session() as session:
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
async def get_musicians()->Musician:
    return get_many_musicians()


@router.get("/musicians/{id}")
async def get_musician_by_id(musician_id: id)->Musician:
    return get_musician(musician_id)


@router.get("/musicians/search?musician={musician_tittle}")
async def get_musicians_by_tittle(musician_tittle: str)->Musician:
    return get_by_tittle(musician_tittle)




@router.post("/musicians")
async def get_musician_by_id(musician: MusicianCreate)->Musician:
    return create_musician(musician)


@router.put("/musicians/{musician_id}")
async def update_new_musician(musician_id: int, musician: MusicianModel)->Musician:
    return update_musician(musician_id, musician)


@router.delete("/musicians/{musician_id}")
async def delete_musician(musician_id: int):
    return delete_musician(musician_id)
