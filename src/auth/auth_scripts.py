from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

import token_config
from schemas import UserInDB
from models import User
from src.database import Session


def verify_password(plain_password, hashed_password):
    return token_config.pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return token_config.pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
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


async def get_current_user(token: Annotated[str, Depends(token_config.oauth2_scheme)]):
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
    with Session() as session:
        user = get_user(db=session, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
