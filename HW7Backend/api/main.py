import csv
import json
import os
import uuid
from typing import List, Optional

import jwt
from fastapi import Form, Response, APIRouter, UploadFile, File, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from models.flowers import Flower
from models.users import User
from models.purchase import Purchase
from repository.FlowerRepository import FlowerRepository
from repository.PurchasesRepository import PurchasesRepository
from repository.UsersRepository import UsersRepository
from pydantic import BaseModel

# Define Pydantic models for API responses
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    avatar: Optional[str] = None

class FlowerResponse(BaseModel):
    id: int
    name: str
    count: int
    price: float

class CartResponse(BaseModel):
    id: int
    name: str
    price: float

class CartSummaryResponse(BaseModel):
    items: List[CartResponse]
    total_price: float

class PurchasedResponse(BaseModel):
    name: str
    price: float

class TokenResponse(BaseModel):
    access_token: str
    type: str = "bearer"

router = APIRouter()
users_repo = UsersRepository()
flower_repo = FlowerRepository()
purchase_repo = PurchasesRepository()
router.mount("/static", StaticFiles(directory="static"), name="static")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_jwt_token(user_id: int) -> str:
    body = {"user_id": user_id}
    token = jwt.encode(body, "nfactor", 'HS256')
    return token

def decode_jwt_token(token) -> int:
    try:
        data = jwt.decode(token, "nfactor", 'HS256')
        return data['user_id']
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def save_img(file_name: str, data):
    with open(file_name, "wb") as img:
        img.write(data)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user_id = decode_jwt_token(token)
    user = users_repo.getUserByID(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@router.post("/signup", status_code=200)
async def signup(email: str = Form(...), pwd: str = Form(...), name: str = Form(...), avatar: UploadFile = File(None)):
    id = len(users_repo.get_all())
    avatar_path = None
    if avatar:
        file_extension = avatar.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join("static/", filename)
        with open(file_path, "wb") as img:
            img.write(await avatar.read())
        avatar_path = file_path
    
    user = User(
        id=id,
        name=name,
        email=email,
        password=pwd,
        avatar=avatar_path
    )
    
    try:
        users_repo.createUser(user)
        return {"status": "success"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(email: str = Form(...), pwd: str = Form(...)):
    user = users_repo.getUserByEmailandPassword(email, pwd)
    if user is not None:
        token = create_jwt_token(user.id)
        return TokenResponse(access_token=token)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

@router.get("/profile")
def profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "avatar": current_user.avatar
    }

@router.get("/flowers")
def get_flowers() -> List[FlowerResponse]:
    flowers = flower_repo.get_all()
    return [
        FlowerResponse(
            id=int(flower.id),
            name=flower.name,
            count=int(flower.count),
            price=float(flower.price)
        ) for flower in flowers
    ]

@router.post("/flowers")
def add_flower(title: str = Form(...), count: str = Form(...), price: str = Form(...)):
    id = len(flower_repo.get_all())
    flower = Flower(
        id=id,
        name=title,
        count=int(count),
        price=float(price),
    )
    flower_repo.add_flower(flower)
    return {"id": id}

@router.post("/cart/items", status_code=200)
def add_to_cart(request: Request, response: Response, flower_id: int = Form(...)):
    # Get existing cart from request cookies
    cart_cookie = request.cookies.get("cart")
    if cart_cookie:
        try:
            cart = json.loads(cart_cookie)
        except:
            cart = []
    else:
        cart = []
    
    if flower_id not in cart:
        cart.append(flower_id)
    
    response.set_cookie(key="cart", value=json.dumps(cart))
    return {"status": "success"}

@router.get("/cart/items")
def get_cart(request: Request) -> CartSummaryResponse:
    try:
        cart_cookie = request.cookies.get("cart")
        cart = json.loads(cart_cookie) if cart_cookie else []
        
        items = []
        total_price = 0
        
        for item_id in cart:
            flower = flower_repo.get_flower_by_id(item_id)
            if flower:
                price = float(flower.price)
                total_price += price
                items.append(CartResponse(
                    id=int(flower.id),
                    name=flower.name,
                    price=price
                ))
        
        return CartSummaryResponse(items=items, total_price=total_price)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/purchased", status_code=200)
def purchased(request: Request, response: Response, current_user: User = Depends(get_current_user)):
    try:
        cart_cookie = request.cookies.get("cart")
        cart = json.loads(cart_cookie) if cart_cookie else []
        
        _id = len(purchase_repo.get_all())
        for item_id in cart:
            purchase_repo.create_purchase(_id, current_user.id, item_id)
            _id += 1
        
        response.delete_cookie("cart")
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/purchased")
def get_purchased(current_user: User = Depends(get_current_user)) -> List[PurchasedResponse]:
    try:
        flowers = purchase_repo.get_purchase_by_flower_id(current_user.id)
        return [
            PurchasedResponse(
                name=flower.name,
                price=float(flower.price)
            ) for flower in flowers
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))







