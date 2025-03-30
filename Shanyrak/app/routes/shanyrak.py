from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.shanyrak import ShanyrakCreate, ShanyrakResponse, ShanyrakUpdate,ShanyrakResponse
from app.repositories.shanyrak import create_shanyrak,get_shanyrak_by_id, update_shanyrak,delete_shanyrak,add_to_favorites, remove_from_favorites, get_user_favorites,filter_shanyraks
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.shanyrak import Shanyrak
from typing import Optional

router = APIRouter(prefix="/shanyraks", tags=["shanyraks"])

@router.get("/favorites", response_model=list[ShanyrakResponse])
def get_favorites(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    favorites = get_user_favorites(db, user)
    return favorites
@router.post("/", response_model=dict)
def create(data: ShanyrakCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    shanyrak = create_shanyrak(db, data, user.id)
    return {"id": shanyrak.id}
@router.get("/{shanyrak_id}", response_model=ShanyrakResponse)
def get_by_id(shanyrak_id: int, db: Session = Depends(get_db)):
    shanyrak = get_shanyrak_by_id(db, shanyrak_id)
    if not shanyrak:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return shanyrak


@router.patch("/{shanyrak_id}")
def update(
        shanyrak_id: int,
        data: ShanyrakUpdate,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    shanyrak = get_shanyrak_by_id(db, shanyrak_id)
    if not shanyrak or shanyrak.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    update_shanyrak(db, shanyrak, data)
    return {"status": "updated"}


@router.delete("/{shanyrak_id}")
def delete(
        shanyrak_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    shanyrak = get_shanyrak_by_id(db, shanyrak_id)
    if not shanyrak or shanyrak.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    delete_shanyrak(db, shanyrak)
    return {"status": "deleted"}
@router.post("/{shanyrak_id}/favorite")
def add_favorite(
    shanyrak_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    add_to_favorites(db, user, shanyrak_id)
    return {"status": "added"}

@router.delete("/{shanyrak_id}/favorite")
def remove_favorite(
    shanyrak_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    remove_from_favorites(db, user, shanyrak_id)
    return {"status": "removed"}

@router.get("/", response_model=list[ShanyrakResponse])
def filter(
    db: Session = Depends(get_db),
    type: Optional[str] = None,
    city: Optional[str] = None,
    price_from: Optional[int] = None,
    price_to: Optional[int] = None,
    rooms_from: Optional[int] = None,
    rooms_to: Optional[int] = None,
):
    return filter_shanyraks(db, type, city, price_from, price_to, rooms_from, rooms_to)