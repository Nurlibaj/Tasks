import csv
import os
from typing import List

from model.cars import Car


class CarRepository:
    def search_by_Name(self,name:str)->Car | None:
        file_path = os.path.join(os.getcwd(), "repository/database", "data.csv")
        cars=[]
        with open(file_path,"r") as file:
            readers=csv.reader(file)
            for row in readers:
                if row[1]==name:
                    cars.append(Car(row[0],row[1],row[2],row[3]))
                    return cars
            return None
    def get_all_cars(self)->List[Car]:
        cars=[]
        try:
            file_path = os.path.join(os.getcwd(), "repository/database", "data.csv")

            with open(file_path,"r") as file:
                readers=csv.reader(file)
                for row in readers:
                    car=Car(
                        id=row[0],
                        name=row[1],
                        color=row[2],
                        year=row[3]
                    )
                    cars.append(car)
                return cars
        except FileNotFoundError:
            print("файл не найден")
            return cars

    def new_car(self,car:Car)->bool:
        cars=list(self.get_all_cars())
        for c in cars:
            if c.name==car.name and c.color==car.color and c.year==car.year:
                return False
        file_path = os.path.join(os.getcwd(), "repository/database", "data.csv")
        with open(file_path,"a",newline="") as file:
            writer=csv.writer(file)
            writer.writerow([len(cars)+1,car.name,car.color,car.year])
            return True


