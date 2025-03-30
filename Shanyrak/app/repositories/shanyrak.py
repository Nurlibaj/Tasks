from sqlalchemy.orm import Session
from app.models.shanyrak import Shanyrak
from app.schemas.shanyrak import ShanyrakCreate,ShanyrakUpdate
from app.models.user import User
from sqlalchemy import and_
from typing import Optional




def create_shanyrak(db: Session, data: ShanyrakCreate, user_id: int) -> Shanyrak:
    shanyrak = Shanyrak(**data.model_dump(), user_id=user_id)
    db.add(shanyrak)
    db.commit()
    db.refresh(shanyrak)
    return shanyrak

def get_shanyrak_by_id(db: Session, shanyrak_id: int) -> Shanyrak | None:
    return db.query(Shanyrak).filter(Shanyrak.id == shanyrak_id).first()

def update_shanyrak(db: Session, shanyrak: Shanyrak, data: ShanyrakUpdate) -> Shanyrak:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(shanyrak, field, value)
    db.commit()
    db.refresh(shanyrak)
    return shanyrak
def delete_shanyrak(db: Session, shanyrak: Shanyrak) -> None:
    db.delete(shanyrak)
    db.commit()
def add_to_favorites(db: Session, user: User, shanyrak_id: int):
    shanyrak = db.query(Shanyrak).filter(Shanyrak.id == shanyrak_id).first()
    if shanyrak and shanyrak not in user.favorites:
        user.favorites.append(shanyrak)
        db.commit()

def remove_from_favorites(db: Session, user: User, shanyrak_id: int):
    shanyrak = db.query(Shanyrak).filter(Shanyrak.id == shanyrak_id).first()
    if shanyrak and shanyrak in user.favorites:
        user.favorites.remove(shanyrak)
        db.commit()

def get_user_favorites(db: Session, user: User) -> list[Shanyrak]:
    return user.favorites
def filter_shanyraks(
    db: Session,
    type: Optional[str],
    city: Optional[str],
    price_from: Optional[int],
    price_to: Optional[int],
    rooms_from: Optional[int],
    rooms_to: Optional[int],
) -> list[Shanyrak]:
    query = db.query(Shanyrak)

    if type:
        query = query.filter(Shanyrak.type == type)
    if city:
        query = query.filter(Shanyrak.address.ilike(f"%{city}%"))
    if price_from is not None:
        query = query.filter(Shanyrak.price >= price_from)
    if price_to is not None:
        query = query.filter(Shanyrak.price <= price_to)
    if rooms_from is not None:
        query = query.filter(Shanyrak.rooms_count >= rooms_from)
    if rooms_to is not None:
        query = query.filter(Shanyrak.rooms_count <= rooms_to)

    return query.all()