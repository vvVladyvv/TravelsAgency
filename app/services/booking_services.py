from app.models.db_booking import Bookings
from app.repositories.Travels_repositories import TravelRepository
from app.repositories.Booking_repositories import BookingRepository
from app.exceptions.bookingExceptions import UnavailableSeats


travel_tools = TravelRepository()
booking_tools = BookingRepository

def reserve_travel(data, db, user_id):
        travel_check = travel_tools.search_travel_by_destination(data.destination)
        totals = data.companions + 1
        if travel_check.available_seats >= totals:

            booking = Bookings(
                travel_id = travel_check.id,
                user_id = user_id,
                companions = totals,
                food_include = travel_check.include_food,
                cost = travel_check.price * totals
            )
        
            return booking_tools.add_booking_db(booking, db)
        raise UnavailableSeats()