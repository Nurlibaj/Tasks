import json
import os
import uuid
from typing import List

import jwt
from fastapi import APIRouter, Depends, File, Form, HTTPException, Response, UploadFile, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db
import models.sql_models as sql_models

router = APIRouter()
router.mount("/static", StaticFiles(directory="static"), name="static")

# OAuth2 setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def create_jwt_token(user_id: int) -> str:
    body = {"user_id": user_id}
    token = jwt.encode(body, "nfactor", algorithm='HS256')
    return token

def decode_jwt_token(token) -> int:
    try:
        data = jwt.decode(token, "nfactor", algorithms=['HS256'])
        if "user_id" not in data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token format",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return data['user_id']
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def save_img(file_name: str, data):
    with open(file_name, "wb") as img:
        img.write(data)

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = decode_jwt_token(token)
    user = crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@router.post("/signup", status_code=200)
async def signup(
    email: str = Form(...), 
    pwd: str = Form(...), 
    name: str = Form(...), 
    avatar: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    # Check if user already exists
    db_user = crud.get_user_by_email(db, email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    avatar_path = None
    if avatar:
        file_extension = avatar.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join("static/", filename)
        with open(file_path, "wb") as img:
            img.write(await avatar.read())
        avatar_path = file_path
    
    user_data = schemas.UserCreate(
        email=email,
        password=pwd,
        name=name
    )
    
    user = crud.create_user(db, user_data, avatar_path)
    return {"status": "success"}

@router.post("/login", response_model=schemas.Token)
def login(
    email: str = Form(...), 
    pwd: str = Form(...),
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_email_and_password(db, email, pwd)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = create_jwt_token(user.id)
    return {"access_token": token, "type": "bearer"}

@router.get("/profile", response_model=schemas.User)
def profile(current_user: sql_models.User = Depends(get_current_user)):
    return current_user

@router.get("/flowers", response_model=List[schemas.Flower])
def get_flowers(db: Session = Depends(get_db)):
    flowers = crud.get_flowers(db)
    return flowers

@router.post("/flowers", response_model=schemas.Flower)
def add_flower(
    title: str = Form(...), 
    count: str = Form(...), 
    price: str = Form(...),
    db: Session = Depends(get_db)
):
    flower_data = schemas.FlowerCreate(
        name=title,
        count=int(count),
        price=float(price)
    )
    flower = crud.create_flower(db, flower_data)
    return flower

@router.patch("/flowers/{flower_id}", response_model=schemas.Flower)
def update_flower(
    flower_id: int,
    flower_update: schemas.FlowerUpdate,
    db: Session = Depends(get_db)
):
    db_flower = crud.update_flower(db, flower_id, flower_update)
    if db_flower is None:
        raise HTTPException(status_code=404, detail="Flower not found")
    return db_flower

@router.delete("/flowers/{flower_id}", status_code=204)
def delete_flower(
    flower_id: int,
    db: Session = Depends(get_db)
):
    success = crud.delete_flower(db, flower_id)
    if not success:
        raise HTTPException(status_code=404, detail="Flower not found")
    return Response(status_code=204)

@router.post("/cart/items", status_code=200)
def add_to_cart(request: Request, response: Response, flower_id: int = Form(...)):
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
    
    result = {"status": "success", "message": "Item added to cart"}
    response = JSONResponse(content=result)
    response.set_cookie(key="cart", value=json.dumps(cart))
    
    return response

@router.get("/cart/items", response_model=schemas.CartSummary)
def get_cart(request: Request, db: Session = Depends(get_db)):
    try:
        cart_cookie = request.cookies.get("cart")
        cart = json.loads(cart_cookie) if cart_cookie else []
        
        items = []
        total_price = 0
        
        for item_id in cart:
            flower = crud.get_flower(db, item_id)
            if flower:
                price = float(flower.price)
                total_price += price
                items.append(schemas.CartItem(
                    id=flower.id,
                    name=flower.name,
                    price=price
                ))
        
        return schemas.CartSummary(items=items, total_price=total_price)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/purchased", status_code=200)
def purchased(
    request: Request, 
    response: Response, 
    current_user: sql_models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        cart_cookie = request.cookies.get("cart")
        cart = json.loads(cart_cookie) if cart_cookie else []
        
        for item_id in cart:
            purchase_data = schemas.PurchaseCreate(
                user_id=current_user.id,
                flower_id=item_id
            )
            crud.create_purchase(db, purchase_data)
        
        response.delete_cookie("cart")
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/purchased", response_model=List[schemas.PurchasedItem])
def get_purchased(
    current_user: sql_models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        flowers = crud.get_purchased_flowers(db, current_user.id)
        return [
            schemas.PurchasedItem(
                name=flower.name,
                price=float(flower.price)
            ) for flower in flowers
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))







