from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi import APIRouter,Form
from fastapi.templating import Jinja2Templates
from pyexpat.errors import messages

from model.cars import Car
from repository.CarsRepository import CarRepository
templates=Jinja2Templates(directory="templates")
car_repo=CarRepository()
car_router=APIRouter(prefix="/cars", tags=["cars"])
@car_router.get("/", status_code=200)
def cars_list(request: Request):
    cars = car_repo.get_all_cars()
    cars=cars[1:]
    message=""
    return templates.TemplateResponse("cars.html", {"request": request, "cars": cars, "message": message})

@car_router.get("/search", status_code=200)
def car_search(request: Request, car_name: str = None):
    if car_name is None:
        cars = []
    else:
        cars = car_repo.search_by_Name(car_name)
    return templates.TemplateResponse("search.html", {"request": request, "cars": cars})
@car_router.get("/new",status_code=200)
def car_create(request:Request):
    return templates.TemplateResponse("new.html",{"request": request})
@car_router.post("/new",status_code=200)
def car_create(request:Request,model:str=Form(...),color:str=Form(...),year:int=Form(...)):
    cars=car_repo.get_all_cars()
    car=Car(len(cars)+1,model,color,year)
    if (car_repo.new_car(car)):
        message="Successfully created new car"
    else:
        message="Car already exists"
    return RedirectResponse(url=f"/cars?message={message}", status_code=303)

