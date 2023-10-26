from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from .schema import *
from ...database.database import get_db
from ...database.models import Users
from sqlalchemy.orm import Session
from ...utils import verify
from .oauth2 import create_access_token

router = APIRouter(tags=["Authentication"])


@router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginUserResp)
def login_user(
    credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user_exists = db.query(Users).filter(credentials.username == Users.email).first()
    if user_exists is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials!!"
        )

    if not verify(credentials.password, user_exists.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials!!"
        )

    access_token = create_access_token({"user_id": user_exists.id})

    return {"access_token": access_token, "token_type": "bearer"}
