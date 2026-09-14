from app.models.db_travels import Travels
from app.models.db_booking import Bookings
from datetime import datetime, timedelta
from app.repositories.Travels_repositories import TravelRepository
from app.exceptions.travelsExceptions import TravelAlreadyExist, TravelNotFound
from sqlalchemy import select, func


travel_tools = TravelRepository()

def create_travel(data,img_uid,db):
    travel = travel_tools.search_travel_by_destination(data.destination, db)
    if travel:
        raise TravelAlreadyExist()

    travel = Travels(
        destination = data.destination,
        activity = data.activity,
        price = data.price,
        available_seats = data.available_seats,
        duration = data.duration,
        image = img_uid
    )

    return travel_tools.add_travel_db(travel, db)



def travel_edit(data, img, db):
    travel = travel_tools.search_travel_by_id(data.id, data)
    if travel:
        travel.destination = data.destination
        travel.activity = data.activity
        travel.price = data.price
        travel.available_seats = data.available_seats
        travel.duration = data.duration
        travel.image = img

        db.commit()
        db.refresh(travel)

        return travel

    raise TravelNotFound()

def get_tendences(db):

    TIME_24H = datetime.now() - timedelta(hours=24)

    seats_sold = func.sum(Bookings.companions).label("seats_sold")

    travels = db.execute(
        select(
            Bookings.travel_id,
            seats_sold
        )
        .where(Bookings.created >= TIME_24H)
        .group_by(Bookings.travel_id)
        .order_by(seats_sold.desc())
    ).all()

    return travels