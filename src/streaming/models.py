import sqlalchemy
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from src.database import base
from src.auth.models import User

metadata = sqlalchemy.MetaData()


class Track(base):
    __tablename__ = "Track"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True)
    author_id= Column(Integer, ForeignKey("Musician.id"))
    genre_id=  Column(Integer, ForeignKey("Genre.id"))
    author = relationship("Musician", back_populates="tracks")
    genre = relationship("Genre", back_populates="tracks")
    date = Column(Date)
    link_to_file = Column(String(100000))


class Musician(base):
    __tablename__ = "Musician"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    tracks = relationship("Track", back_populates="author")
    genre_id = Column(Integer, ForeignKey("Genre.id"))
    genre = relationship("Genre", back_populates="musicians")
    year_start = Column(Integer)
    year_end = Column(Integer)


class Genre(base):
    __tablename__ = "Genre"
    id = Column(Integer, primary_key=True, index=True)
    musicians = relationship("Musician", back_populates="genre")
    tracks = relationship("Track", back_populates="genre")
    title = Column(String(100))


class Playlist(base):
    __tablename__ = "Playlist"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    user_id = Column(Integer, ForeignKey("User.id"))
    user = relationship("User", back_populates="playlists")
