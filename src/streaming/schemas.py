from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from src.auth.schemas import User
# from src.streaming.models import Musician, Genre

# =============Musician Schemas=============#

class MusicianBase(BaseModel):
    id: int
    name: Optional[str] = None
    genre: Optional[str] = None
    year_start:  Optional[int] = None
    year_end:  Optional[int] = None


class Musician(MusicianBase):
    id: int

    class Config:
        orm_mode = True


class MusicianUpdate(MusicianBase):
    pass

class MusicianCreate(MusicianBase):
    id: int
    name: Optional[str] = None
    genre: Optional[str] = None
    year_start:  Optional[int] = None
    year_end:  Optional[int] = None



class MusicianResponse(MusicianBase):
    name: Optional[str] = None
    genre: Optional[str] = None
    year_start:  Optional[int] = None
    year_end:  Optional[int] = None


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
    id: int
    musicians: List[Musician] = []
    title: str | None = None


class GenreResponse(GenreBase):
    id: int
    title: str | None = None
    musicians: List[Musician] = []


    class Config:
        orm_mode = True


# =============Track Schemas=============#
class TrackBase(BaseModel):
    id: int
    title: Optional[str] = None
    author: Optional[Musician] = None
    genre: Optional[Genre] = None
    date: date
    link_to_file: Optional[str] = None


class Track(TrackBase):
    id: int

    class Config:
        orm_mode = True

class TrackCreate(TrackBase):
    title: str
    author: Optional[Musician] = None
    genre: Optional[Genre] = None
    link_to_file: str

class TrackUpdate(TrackBase):
    pass


class TrackResponse(TrackBase):
    id: int
    title: Optional[str] = None
    author: Optional[Musician] = None
    genre: Optional[Genre] = None
    date: date

    class Config:
        orm_mode = True



# =============Playlist Schemas=============#
class PlaylistBase(BaseModel):
    id : int
    name: str

class PlaylistCreate(PlaylistBase):
    user_id: int

class Playlist(PlaylistBase):
    id: int
    user: Optional[User] = None

    class Config:
        orm_mode = True