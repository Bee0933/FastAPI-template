from fastapi import APIRouter, status, HTTPException, Depends, Response
from .schema import *
from ...database.database import get_db
from ...database.models import Users
from sqlalchemy.orm import Session
from typing import List
from ...utils import hash
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CreateUserResp)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    user_exists = db.query(Users).filter(Users.email == user.email).first()

    if user_exists is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="email already exists!!"
        )

    hashed_password = hash(user.password)
    user.password = hashed_password

    new_user = Users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=GetUserResp)
def get_user(id: int, db: Session = Depends(get_db)):
    user_exists = db.query(Users).filter(Users.id == id).first()

    if user_exists is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user does not exist!!"
        )

    return user_exists
