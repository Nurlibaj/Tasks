import csv
from models.purchase import Purchase
from models.flowers import Flower
from repository.FlowerRepository import FlowerRepository
from repository.models.main import FlowerResponse


class PurchasesRepository:
    def __init__(self):
        self.flower_repo = FlowerRepository()
    def get_all(self) -> list[Purchase]:
        purchases = []
        with open("repository/purchased.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 3 and row[0].isdigit():
                    purchases.append(Purchase(
                        id=int(row[0]),
                        user_id=int(row[1]),
                        flower_id=int(row[2])
                    ))
        return purchases
    def create_purchase(self, _id: int, user_id: int, flower_id: int):
        purchase = Purchase(
            id=_id,
            user_id=user_id,
            flower_id=flower_id
        )
        with open("repository/purchased.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([purchase.id, purchase.user_id, purchase.flower_id])

    def get_purchase_by_flower_id(self, user_id: int) -> list[FlowerResponse]:
        ans = []
        purchases = self.get_all()
        flowers_id = []
        
        for purchase in purchases:
            if purchase.user_id == user_id:
                flowers_id.append(purchase.flower_id)

        with open("repository/flowers.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 4 and row[0].isdigit():
                    flower_id = int(row[0])
                    if flower_id in flowers_id:
                        ans.append(FlowerResponse(row[1], float(row[3])))
        return ans



