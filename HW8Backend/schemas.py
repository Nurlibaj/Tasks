from typing import List, Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    avatar: Optional[str] = None

    class Config:
        orm_mode = True


class FlowerBase(BaseModel):
    name: str
    count: int
    price: float

class FlowerCreate(FlowerBase):
    pass

class FlowerUpdate(BaseModel):
    name: Optional[str] = None
    count: Optional[int] = None
    price: Optional[float] = None

class Flower(FlowerBase):
    id: int

    class Config:
        orm_mode = True

class CartItem(BaseModel):
    id: int
    name: str
    price: float

class CartSummary(BaseModel):
    items: List[CartItem]
    total_price: float

class PurchaseBase(BaseModel):
    flower_id: int

class PurchaseCreate(PurchaseBase):
    user_id: int

class Purchase(PurchaseBase):
    id: int
    
    class Config:
        orm_mode = True

class PurchasedItem(BaseModel):
    name: str
    price: float

class Token(BaseModel):
    access_token: str
    type: str = "bearer" 