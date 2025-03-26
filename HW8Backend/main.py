from http.cookiejar import Cookie

import jwt
from fastapi import FastAPI, Form, Response, HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from api.main import router
from models.users import User
from repository.UsersRepository import UsersRepository
import models.sql_models as models
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Flower Marketplace API",
    description="API for a flower marketplace",
    version="1.0.0"
)
app.include_router(router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def get_root():
    return {"message": "Welcome to the Flower Marketplace API"}