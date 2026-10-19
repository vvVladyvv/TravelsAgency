from app.models.db_booking import Bookings
from sqlalchemy import select


class BookingRepository:

    def add_booking_db(self, booking, db):
        db.add(booking)
        db.commit()
        db.refresh(booking)

        return booking

    def get_bookings(self, db):
        bookings = db.query(Bookings).all()
        return bookings

    def user_bookings(self, userId, db):
        stm = (
            select(Bookings)
            .where(Bookings.user_id == userId)
        )

        bookings = db.execute(stm).scalars().all()
        return bookings