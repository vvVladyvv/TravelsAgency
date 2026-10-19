from fastapi import APIRouter, Depends
from app.security.authorization import get_current_user
from sqlalchemy.orm import session
from app.models.db_booking import Bookings

from app.database import get_db
from app.repositories.Booking_repositories import BookingRepository


booking = APIRouter(prefix="/booking", tags=["Booking Services"])

booking_tools = BookingRepository()

@booking.get("/get_bookings")
def get_bookings(db: session = Depends(get_db)):
    return booking_tools.get_bookings(db)


@booking.get("/my_bookings")
def my_bookings(User = Depends(get_current_user), db: session = Depends(get_db)):
    return booking_tools.user_bookings(User["user_id"], db)