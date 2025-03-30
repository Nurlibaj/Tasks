from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse,UserLogin,UserUpdate
from app.models.user import User
from app.db import get_db
from app.core.security import get_password_hash,verify_password, create_access_token
from app.repositories.user import create_user, get_user_by_username,update_user
from fastapi.security import OAuth2PasswordRequestForm
from app.core.dependencies import get_current_user
router = APIRouter(prefix="/auth/users", tags=["auth"])

@router.post("/", response_model=UserResponse)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_username(db, user_create.username)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    hashed_password = get_password_hash(user_create.password)
    user = create_user(db, user_create, hashed_password)
    return user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token}
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
@router.patch("/me", response_model=UserResponse)
def update_me(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated = update_user(db, current_user, update_data)
    return updated