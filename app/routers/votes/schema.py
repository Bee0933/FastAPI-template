from pydantic import BaseModel, conint


class VoteBase(BaseModel):
    post_id: int
    dir: conint(le=1)
