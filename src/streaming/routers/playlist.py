# Управление плейлистами:
# GET /playlists - получение списка плейлистов пользователя
# GET /playlists/{id} - получение конкретного плейлиста пользователя по ID
# POST /playlists - создание нового плейлиста
# PUT /playlists/{id} - обновление существующего плейлиста
# DELETE /playlists/{id} - удаление плейлиста

from fastapi import APIRouter
from src.streaming.schemas import Playlist, PlaylistCreate
from src.streaming.models import Playlist as PlaylistModel
from src.database import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from typing import List

router = APIRouter()


def create_playlist(playlist: PlaylistCreate):
    with Session() as session:
        db_playlist = PlaylistModel(**playlist.dict())

        try:
            session.commit(db_playlist)
            session.refresh(db_playlist)
            return db_playlist
        except SQLAlchemyError as e:
            session.rollback()
            raise HTTPException(status_code=500, detail="Database Error: " + str(e))
    return db_playlist


def get_playlist(playlist_id: int):
    with Session() as session:
        db_playlist = session.query(PlaylistModel).filter(PlaylistModel.id == playlist_id).first()
        if db_playlist is None:
            raise HTTPException(status_code=404, detail="Playlist not found")
        return db_playlist


def get_by_tittle(tittle: str):
    with Session() as session:
        db_playlist = session.query(PlaylistModel).filter(PlaylistModel.tittle == tittle).first()
        if db_playlist is None:
            raise HTTPException(status_code=404, detail="Playlist not found")
        return db_playlist


def get_many_playlists():
    with Session() as session:
        db_playlist = session.query(PlaylistModel).all()
        return db_playlist


def update_playlist(playlist_id: int, playlist: PlaylistModel):
    with Session() as session:
        db_playlist = session.query(PlaylistModel).filter(PlaylistModel.id == playlist_id).first()
        if db_playlist is None:
            raise HTTPException(status_code=404, detail="Playlist not found")
        for field, value in playlist:
            setattr(db_playlist, field, value)
        try:
            session.commit()
            session.refresh(db_playlist)
            return db_playlist
        except  SQLAlchemyError as e:
            session.rollback()
            raise HTTPException(status_code=500, detail="Database Error: " + str(e))


def delete_playlist(playlist_id: int):
    with Session() as session:
        db_playlist = session.query(PlaylistModel).filter(PlaylistModel.id == playlist_id).first()
        if db_playlist is None:
            raise HTTPException(status_code=404, detail="Playlist not found")
        try:
            session.delete(db_playlist)
            session.commit()
        except  SQLAlchemyError as e:
            session.rollback()
            raise HTTPException(status_code=500, detail="Database Error: " + str(e))


@router.get("/playlists")
async def get_playlists() -> List[Playlist]:
    return get_many_playlists()


@router.get("/playlists/{id}")
async def get_playlist_by_id(playlist_id: int) -> Playlist:
    return get_playlist(playlist_id)


@router.get("/playlists/search?playlist={playlist_tittle}")
async def get_playlist_by_tittle(playlist_tittle: str) -> Playlist:
    return get_by_tittle(playlist_tittle)


@router.post("/playlists")
async def create_playlist_(playlist: PlaylistCreate) -> Playlist:
    return create_playlist(playlist)


@router.put("/playlists/{playlist_id}")
async def update_new_playlist(playlist_id: int, playlist: Playlist) -> Playlist:
    return update_playlist(playlist_id, playlist)


@router.delete("/playlists/{playlist_id}")
async def delete_playlist(playlist_id: int):
    return delete_playlist(playlist_id)
