from pydantic import BaseModel, ConfigDict

#----------Input Travels schemas---------------

#Schema for create Travel
class CreateTravel(BaseModel):
    destination: str
    activity: str
    price: int
    available_seats: int
    duration: int
    
    model_config = ConfigDict(from_attributes=True)

#Schema for reserve a travel
class Reserve(BaseModel):
    destination: str
    companions: int
    include_food: bool

