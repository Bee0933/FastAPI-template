from pydantic import BaseModel, EmailStr
from datetime import datetime


class UsersBase(BaseModel):
    email: EmailStr
    password: str


class UsersBaseResp(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class config:
        orm_model = True


class CreateUser(UsersBase):
    pass


class CreateUserResp(UsersBaseResp):
    pass


class GetUserResp(UsersBaseResp):
    pass
