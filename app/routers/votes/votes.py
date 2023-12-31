from fastapi import APIRouter, status, HTTPException, Depends, Response
from .schema import *
from ...database.database import get_db
from ...database.models import Votes
from sqlalchemy.orm import Session
from typing import List
from ..auth import get_current_user
from typing import Optional


router = APIRouter(prefix="/votes", tags={"votes"})


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote_post(
    vote: VoteBase,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    vote_query = db.query(Votes).filter(
        Votes.post_id == vote.post_id, Votes.user_id == current_user.id
    )

    found_vote = vote_query.first()
    # sourcery skip: merge-nested-ifs
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} has already voted on post {vote.post_id}",
            )

        new_vote = Votes(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "succesfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist"
            )

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}
