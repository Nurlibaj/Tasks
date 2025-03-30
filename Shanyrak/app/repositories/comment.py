from sqlalchemy.orm import Session
from app.models.comment import Comment

def create_comment(db: Session, user_id: int, shanyrak_id: int, content: str) -> Comment:
    comment = Comment(
        user_id=user_id,
        shanyrak_id=shanyrak_id,
        content=content
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment
def get_comments_by_shanyrak_id(db: Session, shanyrak_id: int) -> list[Comment]:
    return db.query(Comment).filter(Comment.shanyrak_id == shanyrak_id).all()
def get_comment_by_id(db: Session, comment_id: int) -> Comment | None:
    return db.query(Comment).filter(Comment.id == comment_id).first()

def update_comment(db: Session, comment: Comment, content: str) -> Comment:
    comment.content = content
    db.commit()
    db.refresh(comment)
    return comment
def delete_comment(db: Session, comment: Comment) -> None:
    db.delete(comment)
    db.commit()
