from fastapi import FastAPI

from api.cars import car_router

app = FastAPI()
app.include_router(car_router)
