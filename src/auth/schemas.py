from typing import Optional, List
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str | None = None
    full_name: str | None = None
    hashed_password: str | None = None
    disabled: bool | None = False


    class Config:
        orm_mode = True


class UserCreate(UserBase):
    id: int
    password: str | None = None
    username: str



class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    pass


class UserInDB(UserBase):
    id: int
    username: str
    email: EmailStr
    full_name: str | None = None
    password: str | None = None
    hashed_password: str | None = None
    disabled: bool | None = False



class UserResponse(UserBase):
    id: int
    username: str
    email: EmailStr
    full_name: str | None = None
    disabled: bool | None = False


    class Config:
        orm_mode = True
