from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.repositories.shanyrak import get_shanyrak_by_id
from app.repositories.comment import create_comment,get_comments_by_shanyrak_id,get_comment_by_id,update_comment,delete_comment
from app.schemas.comment import CommentCreate,CommentResponse,CommentUpdate


router = APIRouter(prefix="/shanyraks", tags=["comments"])


@router.post("/{shanyrak_id}/comments")
def create_comment_route(
        shanyrak_id: int,
        data: CommentCreate,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    shanyrak = get_shanyrak_by_id(db, shanyrak_id)
    if not shanyrak:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    create_comment(db, user.id, shanyrak.id, data.content)
    return {"status": "created"}

@router.get("/{shanyrak_id}/comments", response_model=dict)
def get_comments(shanyrak_id: int, db: Session = Depends(get_db)):
    comments = get_comments_by_shanyrak_id(db, shanyrak_id)
    return {
        "comments": [CommentResponse.model_validate(c, from_attributes=True) for c in comments]
    }


@router.patch("/{shanyrak_id}/comments/{comment_id}")
def update_comment_route(
        shanyrak_id: int,
        comment_id: int,
        data: CommentUpdate,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    comment = get_comment_by_id(db, comment_id)
    if not comment or comment.shanyrak_id != shanyrak_id or comment.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    update_comment(db, comment, data.content)
    return {"status": "updated"}


@router.delete("/{shanyrak_id}/comments/{comment_id}")
def delete_comment_route(
        shanyrak_id: int,
        comment_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    comment = get_comment_by_id(db, comment_id)
    if not comment or comment.shanyrak_id != shanyrak_id or comment.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    delete_comment(db, comment)
    return {"status": "deleted"}