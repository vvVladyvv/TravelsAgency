from app.models.db_travels import Travels
from app.repositories.Travels_repositories import TravelRepository
from app.exceptions.travelsExceptions import TravelAlreadyExist, TravelNotFound


travel_tools = TravelRepository()

def create_travel(data,img,db):
    travel = travel_tools.search_travel_by_destination(data.destination, db)
    if travel:
        raise TravelAlreadyExist()

    travel = Travels(
        destination = data.destination,
        activity = data.activity,
        price = data.price,
        available_seats = data.available_seats,
        duration = data.duration,
        image = img
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

