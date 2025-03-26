from attrs import  define
@define
class User:
    id:int
    email:str
    password:str
    name: str
    avatar:str
