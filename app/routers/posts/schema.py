from pydantic import BaseModel
from datetime import datetime
from ..users import UsersBaseResp


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False


class PostBaseResp(PostBase):
    created_at: datetime

    class config:
        orm_model = True


class GetPostsResp(PostBaseResp):
    id: int
    # owner_id: int
    owner: UsersBaseResp


class CreatePosts(PostBase):
    pass


class CreatePostsResp(PostBaseResp):
    id: int
    owner_id: int


class UpdatePosts(PostBase):
    pass


class UpdatePostsResp(PostBaseResp):
    id: int
    owner_id: int


class OutLimit(BaseModel):
    limit: int
