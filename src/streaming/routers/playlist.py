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


def create_playlist(session, playlist: Playlist):
    with session:
        db_playlist = PlaylistModel(**playlist.dict())

        try:
            session.add(db_playlist)
            session.commit()
            session.refresh(db_playlist)
            return db_playlist
        except SQLAlchemyError as e:
            session.rollback()
            raise HTTPException(status_code=500, detail="Database Error: " + str(e))
    return db_playlist


def get_playlist(session, playlist_id: int):
    with session:
        db_playlist = session.query(PlaylistModel).filter(PlaylistModel.id == playlist_id).first()
        if db_playlist is None:
            raise HTTPException(status_code=404, detail="Playlist not found")
        return db_playlist


def get_by_tittle(session, tittle: str):
    with session:
        db_playlist = session.query(PlaylistModel).filter(PlaylistModel.name.like(f'%{tittle.lower()}%')).all()
        if db_playlist is None:
            raise HTTPException(status_code=404, detail="Playlist not found")
        return db_playlist


def get_many_playlists(session):
    with session:
        db_playlist = session.query(PlaylistModel).all()
        return db_playlist


def update_playlist(session, playlist_id: int, playlist: PlaylistModel):
    with session:
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


def delete_playlist(session, playlist_id: int):
    with  session:
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
    with Session() as session:
        return get_many_playlists(session)


@router.get("/playlists/search-playlist-by-tittle")
async def get_playlist_by_tittle(playlist_tittle: str) -> list:
    with Session() as session:
        return get_by_tittle(session, playlist_tittle)


@router.get("/playlists/{id}")
async def get_playlist_by_id(playlist_id: int) -> Playlist:
    with Session() as session:
        return get_playlist(session, playlist_id)


@router.post("/playlists")
async def create_playlist_(playlist: Playlist) -> Playlist:
    with Session() as session:
        return create_playlist(session, playlist)


@router.put("/playlists/{playlist_id}")
async def update_new_playlist(playlist_id: int, playlist: Playlist) -> Playlist:
    with Session() as session:
        return update_playlist(session, playlist_id, playlist)


@router.delete("/playlists/{playlist_id}")
async def delete_playlist(playlist_id: int):
    with Session() as session:
        return delete_playlist(session, playlist_id)
