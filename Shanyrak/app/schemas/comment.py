from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommentCreate(BaseModel):
    content: str

class CommentUpdate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: int
    content: str
    created_at: Optional[datetime] = None
    user_id: int  # ← это соответствует модели

    class Config:
        orm_mode = True

