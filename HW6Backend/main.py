from http.cookiejar import Cookie

import jwt
from fastapi import FastAPI, Form, Response,HTTPException
from fastapi.openapi.models import Response
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from api.main import router
from models import users
from models.users import User
from repository.UsersRepository import UsersRepository

templates = Jinja2Templates(directory="templates")

app=FastAPI()
app.include_router(router)
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/")
def get_root(request:Request):
    return {"main page"}