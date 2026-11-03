from app.models.db_travels import Travels
from sqlalchemy import select


class TravelRepository:

    def search_travel_by_destination(self, travel_destination, db):
        return db.execute(
            select(Travels).where(Travels.destination == travel_destination)).scalars().first()
        

    def search_travel_by_id(self, travel_id, db):
        return db.execute(
            select(Travels).where(Travels.id == travel_id)).scalars().first()
        

    def add_travel_db(self, travel, db):
        db.add(travel)
        db.commit()
        db.refresh(travel)

        return travel

    def get_all_travels(self, db):
        return db.execute(select(Travels)).scalars().all()

    def edit_travel(self, travel, db):
        db.commit()
        db.refresh(travel)

        return travel

    def delete_travel(self, travel, db):
        db.delete(travel)
        db.commit()
