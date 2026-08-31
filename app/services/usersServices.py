from app.models.db_user import Users
from fastapi import HTTPException
from app.repositories.Users_repositories import (
    UserRepository, 
)
from app.exceptions.userExceptions import (
    UserAlreadyExist, InvalidCredentials, UserNotFound
)
from app.security.jwt import create_token
from app.security.hashing import(
    hashed_password, verify_password
)

user_tools = UserRepository()

def add_new_user(data, image_uuid,db):
    user = user_tools.found_user_by_email(data.email, db)
    if user:
        raise UserAlreadyExist()

    new_user = Users(
        username = data.username,
        age = data.age,
        email = data.email,
        password = hashed_password(data.password),
        image = image_uuid
    )

    return user_tools.add_user_db(new_user, db)
 

def verified_user(data, db):
    user = user_tools.found_user_by_email(data.email, db)
    if user and verify_password(data.password, user.password):
        token = create_token({"user_id": user.id, "user_name": user.username, "role": user.role})
        return {
            "message": "Authenticated",
            "access_token": token,
            "token_type": "bearer"
            }       
    raise InvalidCredentials()


def user_edit(data, db):
    checked = user_tools.found_user_by_id(data.id, db)
    if checked:
        checked.username = data.username
        checked.age = data.age
        checked.email = data.email

        db.commit()
        return checked
    raise UserNotFound()


def admin_role(data, db):
    user = user_tools.found_user_by_id(data, db)
    if user:
        user.role = "admin",
        db.commit()
        return user
    raise UserNotFound()