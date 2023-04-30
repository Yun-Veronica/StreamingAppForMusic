from fastapi import APIRouter, Depends, HTTPException, status
from src.database import Session
from fastapi.security import OAuth2PasswordRequestForm
from auth_scripts import get_current_active_user, authenticate_user, create_access_token, get_current_user, get_user, \
    get_password_hash
from schemas import User, UserCreate, UserInDB, UserUpdate
from token_config import Token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from typing import Annotated
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()


# @router.get("/users/me/", response_model=User, tags=["users"])
# async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
#     return current_user


@router.get("/users/{username}", tags=["users"])
async def read_user(username: Annotated[User, Depends(get_current_active_user)]):
    return {"username": username}


# @router.post("/register/", tags=["users"])
# async def register(username: Annotated[User, Depends(get_current_active_user)]):
#     return {"username": username}


@router.post("/login/", tags=["users"])
async def login(username: Annotated[User, Depends(get_current_active_user)]):
    return {"username": username}


@router.post("/register/", tags=["users"])
async def register_user(user: UserCreate):
    db_user = get_user(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict.pop("password")
    with Session() as session:
        user_in_db = UserInDB(**user_dict, hashed_password=hashed_password)
        session.add(user_in_db)
        try:
            session.commit(User)
            session.refresh(User)
            return user_in_db
        except SQLAlchemyError as e:
            session.rollback()
            raise HTTPException(status_code=500, detail="Database Error: " + str(e))
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    with Session() as session:
        user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.put("/users/{username}", response_model=User)
async def update_user(username: str, user: UserUpdate, db: Session, current_user: User = Depends(get_current_user)):
    # Check if the user exists
    db_user = get_user(db, username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    # Check if the user has permission to update the user
    if current_user.username != username:
        raise HTTPException(status_code=403, detail="You don't have permission to update this user")
    # Update the user
    db_user = update_user(db, db_user=db_user, user=user)
    # Return the updated user
    return db_user


@router.delete("/users/{username}", tags=["users"])
async def delete_user(username: Annotated[User, Depends(get_current_active_user)]):
    return {"username": username}
