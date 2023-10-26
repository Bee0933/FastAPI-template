from fastapi import APIRouter, status, HTTPException, Depends, Response
from .schema import *
from ...database.database import get_db
from ...database.models import Posts
from sqlalchemy.orm import Session
from typing import List
from ..auth import get_current_user
from typing import Optional

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[GetPostsResp])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
    limit: int = 5,
    skip: int = 0,
    search: Optional[str] = "",
):
    return (
        db.query(Posts)
        .filter(Posts.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=GetPostsResp)
def get_posts(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    post_exist = db.query(Posts).filter(Posts.id == id).first()
    if post_exist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="resource no found!!"
        )

    if post_exist.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="not authorized to perform requested action!",
        )

    return post_exist


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CreatePostsResp)
def create_post(
    post: CreatePosts,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    new_post = Posts(owner_id=current_user.id, **post.model_dump())
    # new_post.owner_id = current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.put(
    "/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=UpdatePostsResp
)
def update_post(
    id: int,
    post_update: UpdatePosts,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    update_post = db.query(Posts).filter(Posts.id == id)
    post_exist = update_post.first()

    if post_exist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="resource no found!!"
        )

    if post_exist.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="not authorized to perform requested action!",
        )

    update_post.update(post_update.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(post_exist)

    return post_exist


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    del_post = db.query(Posts).filter(Posts.id == id)
    post_exist = del_post.first()

    if post_exist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="resource no found!!"
        )

    if post_exist.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="not authorized to perform requested action!",
        )

    del_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
