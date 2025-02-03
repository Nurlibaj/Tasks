import csv

from models.flowers import Flower
class FlowerRepository:
    def get_all(self)->list[Flower]:
        flowers=[]
        with open("repository/flowers.csv", "r") as file:
            reader=csv.reader(file)
            for row in reader:
                flower=Flower(row[0],row[1],row[2],row[3])
                flowers.append(flower)
            return flowers
    def add_flower(self, flower: Flower):
        with open("repository/flowers.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([flower.id, flower.name, flower.count, flower.price])
    def get_flower_by_id(self,flower_id:int)->list[Flower]:
        with open("repository/flowers.csv", "r") as file:
            reader=csv.reader(file)
            for row in reader:
                if row[0]==str(flower_id):
                    return Flower(int(row[0]),row[1],int(row[2]),row[3])