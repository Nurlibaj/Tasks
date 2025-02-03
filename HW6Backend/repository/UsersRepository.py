import csv

from models import users
from models.users import User


class UsersRepository:
    def createUser(self,user:User):
        if self.verifyUserByEmail(user.email):
            raise ValueError("User already exists")
        with open("repository/users.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([user.id,user.email,user.password,user.name,user.avatar])
    def verifyUserByEmail(self,email:str):
        with open("repository/users.csv","r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row[1] == email:
                    return True
        return False
    def getUserByID(self,user_id:int)->User | None:
        with open("repository/users.csv","r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == str(user_id):
                    return User(int(row[0]),row[1],row[2],row[3],row[4])
        return None
    def getUserByEmailandPassword(self,email:str,pwd:str)->User | None:
        with open("repository/users.csv","r") as f:
            reader=csv.reader(f)
            for row in reader:

                if row[1] == email and row[2] == pwd:
                    print("running")
                    return User(int(row[0]),row[1],row[2],row[3],row[4])
        return None
    def get_all(self):
        users=[]
        with open("repository/users.csv","r") as f:
            reader=csv.reader(f)
            for row in reader:
                users.append(User(row[0],row[1],row[2],row[3],row[4]))
        return users


