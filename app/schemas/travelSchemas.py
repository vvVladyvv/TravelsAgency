from pydantic import BaseModel, ConfigDict, field_validator

#----------Input Travels schemas---------------

#Shared travel fields used by input and response schemas
class TravelBase(BaseModel):
    destination: str
    activity: str
    price: int
    available_seats: int
    duration: int
    image: str

    model_config = ConfigDict(from_attributes=True)


#Schema for create Travel
class CreateTravel(TravelBase):

    @field_validator('destination')
    @classmethod
    def destination_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Destination must not be empty')
        return v.strip()
    
    @field_validator('activity')
    @classmethod
    def activity_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Activity must not be empty')
        return v.strip()

    @field_validator('available_seats')
    @classmethod
    def available_seats_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Available seats must be a positive integer and greater than 0')
        return v
    

    @field_validator('price')
    @classmethod
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be a positive integer and greater than 0')
        return v

    @field_validator('duration')
    @classmethod
    def duration_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Duration must be a positive integer and greater than 0')
        return v



class TravelResponse(TravelBase):
    pass

#Schema for reserve a travel
class Reserve(BaseModel):
    destination: str
    companions: int
    include_food: bool

