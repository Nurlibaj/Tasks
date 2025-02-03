import csv
from models import purchase
from models import flowers
from models.flowers import Flower
from repository.FlowerRepository import FlowerRepository
from repository.models.main import FlowerResponse, get_all_response


class PurchasesRepository:
    def __init__(self):
        flower_repo=FlowerRepository()
    def get_all(self)->list[get_all_response]:
        purchase=[]
        with open("repository/purchased.csv","r") as file:
            reader=csv.reader(file)
            for row in reader:
                if row[1]>="0" and row[1]<"9":
                    purchase.append(get_all_response(int(row[1]),int(row[2])))
        return purchase
    def create_purchase(self,_id:int,user_id:int,flower_id:int):
        with open("repository/purchased.csv","a",newline="") as file:
            writer=csv.writer(file)
            writer.writerow([_id,user_id,flower_id])

    def get_purchase_by_flower_id(self,user_id:int)->list[FlowerResponse]:
        ans=[]
        purchases=self.get_all()
        flowers_id=[]
        for item in purchases:
            if item.user_id==user_id:
                flowers_id.append(item.flower_id)

        with open("repository/flowers.csv","r") as file:
            reader=csv.reader(file)
            for row in reader:
                for j in range(len(flowers_id)):
                    if row[0]>='0' and row[0]<='9':
                        if int(row[0])==flowers_id[j]:
                            ans.append(FlowerResponse(row[1],float(row[3])))
        return  ans



