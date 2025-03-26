from attrs import define
@define
class FlowerResponse:
    name:str
    price:float
@define
class get_all_response:
    user_id:int
    flower_id:int