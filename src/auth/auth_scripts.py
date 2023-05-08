from datetime import datetime, timedelta
from typing import Annotated
from sqlalchemy import literal_column
from sqlalchemy.exc import SQLAlchemyError

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from src.auth import token_config
from src.auth.schemas import UserInDB
from src.auth.models import User
from src.database import Session


def verify_password(plain_password, hashed_password):
    return token_config.pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return token_config.pwd_context.hash(password)
#TODO DELETE

# def create_new_user(user: User):
#     with Session() as session:
#         db_user = User(**user.dict())
#
#         try:
#             session.add(db_user)
#             session.commit()
#             session.refresh(db_user)
#             return db_user
#         except SQLAlchemyError as e:
#             session.rollback()
#             raise HTTPException(status_code=500, detail="Database Error: " + str(e))
#     return db_user

def get_user_username(session, username: str):
    with session:
        user = session.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        # return UserInDB(**user)
        return user
def get_user_username_(session, username: str):
    with session:
        user_db = session.query(User).filter(User.username == username).first()
        if user_db is None:
            raise HTTPException(status_code=404, detail="User not found")

        return user_db


# TODO CHANGE Session()
def get_user_id(user_id: int):
    with Session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return UserInDB(**user)
def authenticate_user(db,username: str, password: str):
    user = get_user_username_(session=db,username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, token_config.SECRET_KEY, algorithm=token_config.ALGORITHM)
    return encoded_jwt


def get_current_user(session,token: Annotated[str, Depends(token_config.oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, token_config.SECRET_KEY, algorithms=[token_config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = token_config.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    # TODO CHANGE Session()

    with Session() as session:
        user = get_user_username(session=session,username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
