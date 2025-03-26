import csv

from models.flowers import Flower
class FlowerRepository:
    def get_all(self)->list[Flower]:
        flowers=[]
        with open("repository/flowers.csv", "r") as file:
            reader=csv.reader(file)
            for row in reader:
                if len(row) >= 4:
                    try:
                        flower = Flower(
                            id=int(row[0]),
                            name=row[1],
                            count=int(row[2]),
                            price=float(row[3])
                        )
                        flowers.append(flower)
                    except (ValueError, IndexError):
                        # Skip invalid rows
                        pass
            return flowers
    def add_flower(self, flower: Flower):
        with open("repository/flowers.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([flower.id, flower.name, flower.count, flower.price])
    def get_flower_by_id(self,flower_id:int)->Flower:
        with open("repository/flowers.csv", "r") as file:
            reader=csv.reader(file)
            for row in reader:
                if len(row) >= 4 and row[0].isdigit() and int(row[0]) == flower_id:
                    return Flower(
                        id=int(row[0]),
                        name=row[1],
                        count=int(row[2]),
                        price=float(row[3])
                    )
        return None