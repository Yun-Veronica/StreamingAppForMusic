import sqlalchemy
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from src.database import base

metadata = sqlalchemy.MetaData()


class User(base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    full_name = Column(String(100))
    hashed_password = Column(String(1000), unique=True, index=True)
    disabled = Column(Boolean)
    playlists = relationship("Playlist", back_populates="user")
