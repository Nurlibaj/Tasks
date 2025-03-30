from pydantic import BaseModel
from typing import Optional

class ShanyrakCreate(BaseModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: Optional[str] = None

class ShanyrakUpdate(BaseModel):
    type: Optional[str]
    price: Optional[int]
    address: Optional[str]
    area: Optional[float]
    rooms_count: Optional[int]
    description: Optional[str]

class ShanyrakResponse(BaseModel):
    id: int
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: Optional[str]
    user_id: int

    class Config:
        orm_mode = True
