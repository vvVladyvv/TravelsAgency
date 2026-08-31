from fastapi import APIRouter, Depends, HTTPException, status, Form, UploadFile, File

from sqlalchemy.orm import Session
from app.models.db_user import Users
from app.schemas.usersSchemas import UserRegister, UserLogin, UserResponse, LoginResponse, UserEdit
from app.database import get_db
from app.services.usersServices import add_new_user, verified_user, admin_role
from app.security.authorization import get_current_user, get_admin
from app.security.hashing import hashed_password
from fastapi.responses import FileResponse
from app.exceptions.userExceptions import AdminRequired, UserNotFound
from app.repositories.Users_repositories import UserRepository


user = APIRouter(prefix='/user', tags=["User services"])
user_maintain = APIRouter(prefix='/user_maintain', tags=["User Maintain"])
user_tools = UserRepository()

@user.get("/")
async def read_index():
    return FileResponse("index.html")

@user.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(data: UserRegister, db: Session = Depends(get_db)):
    user = add_new_user(data, db)
    return user

@user.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login_user(data: UserLogin, db: Session = Depends(get_db)):
    token = verified_user(data, db)
    return token

@user_maintain.get("/get_users", response_model=list[UserResponse])
def get_users(Admin = Depends(get_admin), db: Session = Depends(get_db)):
    if Admin:
        user = db.query(Users).all()
        return user
    raise AdminRequired()


@user_maintain.post("/get_user", response_model=UserResponse)
def get_user(user_id: int, admin = Depends(get_admin), db: Session = Depends(get_db)):
    if admin:
        user = user_tools.found_user_by_id(user_id, db)
        return user
    raise AdminRequired()

@user_maintain.put("/edit_user", response_model=UserResponse)
def edit_user(userId: int = Form(...), new_username: str = Form(...), new_age: int = Form(...), new_email: str = Form(...), new_password: str = Form(...), new_image: UploadFile = File(...), Admin = Depends(get_admin), db: Session = Depends(get_db)):
    if Admin:
        new_user = UserRegister(
            username=new_username,
            age=new_age,
            email=new_email,
            password=new_password
        )
        check = user_tools.found_user_by_id(userId, db)
        if check:
            check.username = new_user.username
            check.age = new_user.age
            check.email = new_user.email
            check.password = hashed_password(new_user.password)

            db.commit()
            db.refresh(check)
        raise UserNotFound()

    raise AdminRequired()


@user_maintain.delete("/delete_user", response_model=UserResponse)
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



