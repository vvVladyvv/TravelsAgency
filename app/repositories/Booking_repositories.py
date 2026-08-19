from app.models.db_booking import Bookings


class BookingRepository:

    def add_booking_db(self, booking, db):
        db.add(booking)
        db.commit()
        db.refresh(booking)

        return booking