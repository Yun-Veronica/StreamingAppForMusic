from pydantic import BaseModel
from datetime import date
from typing import List
from src.auth.schemas import User


# from src.streaming.model import Musician, Genre

# =============Musician Schemas=============#

class MusicianBase(BaseModel):
    id: int
    name: str | None = None
    # genre: str | None = None
    genre_id: int | None = None
    year_start: int | None = None
    year_end: int | None = None


class Musician(MusicianBase):
    id: int

    class Config:
        orm_mode = True


class MusicianUpdate(MusicianBase):
    pass


class MusicianCreate(MusicianBase):
    id: int
    name: str | None = None
    genre_id: int | None = None
    year_start: int | None = None
    year_end: int | None = None


class MusicianResponse(MusicianBase):
    id: int | None = None
    name: str | None = None
    # genre: str | None = None
    year_start: int | None = None
    year_end: int | None = None

    class Config:
        orm_mode = True


# =============Genre Schemas=============#

class GenreBase(BaseModel):
    id: int
    title: str | None = None


class Genre(GenreBase):
    id: int

    class Config:
        orm_mode = True


class GenreUpdate(GenreBase):
    pass


class GenreCreate(GenreBase):
    pass


class GenreResponse(GenreBase):
    id: int
    title: str | None = None

    class Config:
        orm_mode = True


# =============Track Schemas=============#
class TrackBase(BaseModel):
    id: int
    title: str | None = None
    author_id: int | None = None
    genre_id: int | None = None
    date: date
    link_to_file: str | None = None


class Track(TrackBase):
    id: int
    title: str | None = None
    author_id: int | None = None
    genre_id: int | None = None
    date: date
    link_to_file: str | None = None
    class Config:
        orm_mode = True


class TrackCreate(TrackBase):
    title: str
    # author: Musician | None = None
    # genre: Genre | None = None
    link_to_file: str


class TrackUpdate(TrackBase):
    pass


class TrackResponse(TrackBase):
    id: int
    title: str | None = None
    # author: Musician | None = None
    # genre: Genre | None = None
    date: date

    class Config:
        orm_mode = True


# =============Playlist Schemas=============#
class PlaylistBase(BaseModel):
    id: int
    name: str


class PlaylistCreate(PlaylistBase):
    user_id: int


class Playlist(PlaylistBase):
    id: int
    user: User | None = None

    class Config:
        orm_mode = True
