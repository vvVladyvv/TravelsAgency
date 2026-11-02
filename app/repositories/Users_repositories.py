from app.models.db_user import Users
from sqlalchemy import select

class UserRepository:
    
    def found_user_by_email(self, user_email, db):
        return db.execute(
            select(Users).where(Users.email == user_email)).scalars().first()

    def found_user_by_id(self, user_id, db):
        return db.execute(
            select(Users).where(Users.id == user_id)).scalars().first()

    def add_user_db(self, user, db):
        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    def get_users(db):
        return db.execute(
            select(Users)).all
    
    def delete_user(self, user, db):
        db.delete(user)
        db.commit()

    def update_user(self, user, db):
        db.commit()
        db.refresh(user)
        return user

