from pydantic import BaseModel

#----------Input Travels schemas---------------

#Schema for create Travel
class CreateTravel(BaseModel):
    destination: str
    activity: str
    price: int
    available_seats: int
    duration: int

#Schema for edit a Travel
class TravelEdit(CreateTravel):
    id: int

#Schema for reserve a travel
class Reserve(BaseModel):
    destination: str
    companions: int
    include_food: bool

