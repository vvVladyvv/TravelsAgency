from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.schemas.travelSchemas import CreateTravel

class BookingBase(BaseModel):
    travel_id: int
    user_id: int
    created: Optional[datetime] = None

class BookingResponse(BookingBase):
    id: int
    companions: int
    food_include: bool
    status: str
    cost: float

    travel: CreateTravel

    model_config = ConfigDict(from_attributes=True)