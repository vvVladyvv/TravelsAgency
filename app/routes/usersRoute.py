from fastapi import APIRouter, Depends, HTTPException,status

from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.db_user import Users
from app.schemas.usersSchemas import UserRegister, UserLogin, RegisterResponse, LoginResponse, UserEdit
from app.database import get_db
from app.services.usersServices import add_new_user, verified_user, user_edit, admin_role
from app.security.authorization import get_current_user, get_admin
from fastapi.responses import FileResponse
from app.exceptions.userExceptions import AdminRequired
from app.repositories.Users_repositories import UserRepository


user = APIRouter(prefix='/user', tags=["User services"])
user_maintain = APIRouter(prefix='/user_maintain', tags=["User Maintain"])
user_tools = UserRepository()

@user.get("/")
async def read_index():
    return FileResponse("index.html")

@user.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register_user(data: UserRegister, db: Session = Depends(get_db)):
    user = add_new_user(data, db)
    return user

@user.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login_user(data: UserLogin, db: Session = Depends(get_db)):
    token = verified_user(data, db)
    return token

@user_maintain.get("/get_users")
def get_users(user = Depends(get_admin), db: Session = Depends(get_db)):
    if user:
        user = db.query(Users).all()
        return user
    raise AdminRequired()

@user_maintain.post("/get_user")
def get_user(user_id: int, admin = Depends(AdminRequired), db: Session = Depends(get_db)):
    if admin:
        return db.query(Users).filter(Users.id == user_id).first()
                

@user_maintain.put("/edit_user")
def edit_user(data: UserEdit, Admin = Depends(get_admin), db: Session = Depends(get_db)):
    if Admin:
        user = user_edit(data, db)
        return user
    raise AdminRequired()


@user_maintain.delete("/delete_user")
def delete_user(id: int, Admin = Depends(get_admin), db: Session = Depends(get_db)):
    if Admin:
        user = user_tools.found_user_by_id(id, db)
        if user:
            db.delete(user)
            db.commit()

            return user
        raise HTTPException(status_code=404, detail="User was not found")
    raise AdminRequired()

@user.get("/current_user")
def get_actual_user(user = Depends(get_current_user)):
    return user

@user_maintain.post("/get_admin")
def get_admin_role(id: int, db: Session = Depends(get_db)):
    return admin_role(id, db)



