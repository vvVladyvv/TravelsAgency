from pydantic import BaseModel


class CreateTravel(BaseModel):
    destination: str
    activity: str
    price: int
    available_seats: int
    duration: int

class TravelEdit(CreateTravel):
    id: int

class Reserve(BaseModel):
    destination: str
    companions: int
    include_food: bool

