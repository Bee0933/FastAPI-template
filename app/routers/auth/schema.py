from pydantic import BaseModel, EmailStr
from typing import Optional


class LoginBase(BaseModel):
    email: EmailStr
    password: str


class TokenData(BaseModel):
    id: Optional[str] = None


class LoginUser(LoginBase):
    pass


class LoginUserResp(BaseModel):
    access_token: str
    token_type: str
