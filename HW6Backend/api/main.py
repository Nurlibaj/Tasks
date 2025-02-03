
import csv
import json
import os
import uuid
from urllib import request

import jwt
from fastapi import Form, Response, APIRouter, UploadFile, File, HTTPException
from fastapi import Response

from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from models.flowers import Flower
from models.users import User
from repository.FlowerRepository import FlowerRepository
from repository.PurchasesRepository import PurchasesRepository
from repository.UsersRepository import UsersRepository

templates = Jinja2Templates(directory="templates")

router = APIRouter()
users_repo = UsersRepository()
flower_repo=FlowerRepository()
purchase_repo=PurchasesRepository()
router.mount("/static", StaticFiles(directory="static"), name="static")
def create_jwt_token(user_id: int) -> str:
    body = {"user_id": user_id}
    token = jwt.encode(body, "nfactor", 'HS256')
    return token
def decode_jwt_token(token) -> int:
    data = jwt.decode(token, "nfactor", 'HS256')
    return data['user_id']
def save_img(file_name: str,data):
    with open("repository/users.csv", mode="a", newline= "") as img:
        writer = csv.DictWriter(img, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

@router.get("/signup")
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.post("/signup")
async def signup(request: Request, email: str = Form(...), pwd: str = Form(...), name: str = Form(...),avatar:UploadFile = File(None)):
    id = len(users_repo.get_all())
    avatar_path=None
    if avatar:
        file_extension=avatar.filename.split(".")[-1]
        filename=f"{uuid.uuid4()}.{file_extension}"
        file_path=os.path.join("static/", filename)
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
        return RedirectResponse(url="/login", status_code=303)
    except ValueError as e:
        return templates.TemplateResponse("signup.html", {"request": request, "error": e})


@router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login(request: Request, response: Response, email: str = Form(...), pwd: str = Form(...)):
    user = users_repo.getUserByEmailandPassword(email, pwd)
    if user is not None:
        token = create_jwt_token(user.id)
        response = RedirectResponse(url="/profile", status_code=303)
        response.set_cookie(key="publickey", value=token, secure=False)
        return response
    return templates.TemplateResponse("login.html", {"request": request, "error": "Incorrect email or password"})
@router.get("/users")
async def get_users(request:Request):
    users=users_repo.get_all()
    return [{"id":user.id,"name":user.name,"email":user.email,"pwd":user.password, "avatar":user.avatar} for user in users]

@router.get("/profile")
def profile(request: Request):
    token = request.cookies.get("publickey")
    if token is None:
        return RedirectResponse(url="/login", status_code=303,headers={"error_message":"Access denied"})
    user_id=decode_jwt_token(token)
    user=users_repo.getUserByID(user_id)
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})

@router.get("/flowers")
def get_flowers(request: Request):
    token = request.cookies.get("publickey")
    if token is None:
        return RedirectResponse(url="/login", status_code=303,headers={"error_message":"Access denied"})
    flowers=flower_repo.get_all()
    flowers=flowers[1:]
    return templates.TemplateResponse("flowers.html", {"request": request,"flowers":flowers})
@router.post("/flowers")
def add_flower(request: Request, title:str = Form(...), count:str = Form(...), price:str = Form(...)):
    id=len(flower_repo.get_all())
    flower=Flower(
        id=id,
        name=title,
        count=int(count),
        price=int(price),
    )
    flower_repo.add_flower(flower)
    return RedirectResponse(url="/flowers",status_code=303)
@router.post("/cart/items")
def add_to_cart(request: Request,response: Response, flower_id:int=Form(...)):
    cart=request.cookies.get("cart")
    if cart is None:
        cart=[]
    else:
        cart=json.loads(cart)
    if flower_id not in cart:
        cart.append(flower_id)
    else:
        pass
    response = RedirectResponse(url="/flowers", status_code=303)
    response.set_cookie(key="cart", value=json.dumps(cart))
    return response
@router.get("/cart/items")
def get_cart(request: Request):
    try:
        cart=json.loads(request.cookies.get("cart"))
        if cart is None:
            cart = []
        flowers_cart=[]
        total_price=0
        for item in cart:
            flower=flower_repo.get_flower_by_id(item)
            total_price+=float(flower.price)
            flowers_cart.append(flower)
        return templates.TemplateResponse("cart.html",{"request":request,"flowers":flowers_cart,"total_price":total_price})
    except:
        raise ValueError("cookie is deleted")
@router.post("/purchased")
def purchased(request: Request, response: Response):
    try:
        user_id=request.cookies.get("publickey")
        user_id=decode_jwt_token(user_id)
        if not user_id:
            raise HTTPException(status_code=404, detail="User not found")
        cart=json.loads(request.cookies.get("cart"))
        if cart is None:
            cart=[]
        _id=len(purchase_repo.get_all())
        for item in cart:
            purchase_repo.create_purchase(_id,user_id,item)
            _id+=1
        return RedirectResponse(url="/purchased",status_code=303)
        response.delete_cookie("cart")
    except:
        raise ValueError("cookie is deleted")
@router.get("/purchased")
def get_purchased(request: Request):
    flowers=[]
    try:
        user_cookie=request.cookies.get("publickey")
        user_id=decode_jwt_token(user_cookie)
        if not user_id:
            raise HTTPException(status_code=404, detail="User not found")
        flowers= purchase_repo.get_purchase_by_flower_id(user_id)
        return templates.TemplateResponse("purchased.html",{"request":request,"flowers":flowers})
    except:
        return RedirectResponse(url="/login",status_code=303)







