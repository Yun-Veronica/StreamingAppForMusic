import sqlalchemy
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from src.database import base

metadata = sqlalchemy.MetaData()


class Track(base):
    __tablename__ = "Track"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = relationship("Musician", back_populates="Track")
    genre = relationship("Genre", back_populates="Track")
    date = Column(Date)
    link_to_file = Column(String)


class Musician(base):
    __tablename__ = "Musician"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    tracks = relationship("Track", back_populates="Musician")
    genre = relationship("Genre", back_populates="Musician")
    year_start = Column(Integer)
    year_end = Column(Integer)


class Genre(base):
    __tablename__ = "Genre"
    id = Column(Integer, primary_key=True, index=True)
    musicians = relationship("Musician", back_populates="Genre")
    tracks = relationship("Track", back_populates="Genre")
    title = Column(String, index=True)


class Playlist(base):
    __tablename__ = "Playlist"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="Playlist")
