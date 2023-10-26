from datetime import timezone
from jose import JWTError, jwt
from decouple import config
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import schema
from ...database import get_db, Users
from sqlalchemy.orm import Session
from ...config import Settings

settings = Settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict) -> jwt:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=int(settings.jwt_token_time_minuites)
    )
    to_encode["exp"] = expire

    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.algorithm)


def verify_access_token(token: str, credentials_exception):
    # sourcery skip: avoid-builtin-shadow
    try:
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.algorithm]
        )

        id: str = str(payload.get("user_id"))

        if id is None:
            raise credentials_exception

        token_data = schema.TokenData(id=id)
    except JWTError as e:
        raise credentials_exception from e
    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="not authenticated!",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(
        token=token, credentials_exception=credentials_exception
    )

    return db.query(Users).filter(Users.id == token.id).first()
