from typing import Optional, List
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    id: Optional[int]
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    hashed_password: str
    disabled: Optional[bool] = False


    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str
    username: str



class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str


class UserResponse(UserBase):
    id: Optional[int]
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    disabled: Optional[bool] = False


    class Config:
        orm_mode = True
