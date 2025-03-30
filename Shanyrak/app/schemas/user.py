from pydantic import BaseModel, EmailStr
from typing import Optional

class UserUpdate(BaseModel):
    phone: Optional[str] = None
    name: Optional[str] = None
    city: Optional[str] = None

class UserCreate(BaseModel):
    username: EmailStr
    password: str
    phone: Optional[str] = None
    name: Optional[str] = None
    city: Optional[str] = None

class UserLogin(BaseModel):
    username: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: EmailStr
    phone: Optional[str] = None
    name: Optional[str] = None
    city: Optional[str] = None

    class Config:
        orm_mode = True
