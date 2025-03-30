from fastapi import FastAPI
from app.routes import auth,shanyrak,comments

app = FastAPI()

app.include_router(auth.router)
app.include_router(shanyrak.router)
app.include_router(comments.router)