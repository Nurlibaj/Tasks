from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate,UserUpdate

def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user_create: UserCreate, hashed_password: str) -> User:
    user = User(
        username=user_create.username,
        password=hashed_password,
        phone=user_create.phone,
        name=user_create.name,
        city=user_create.city
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()
from app.schemas.user import UserUpdate

def update_user(db: Session, user: User, update_data: UserUpdate) -> User:
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user
