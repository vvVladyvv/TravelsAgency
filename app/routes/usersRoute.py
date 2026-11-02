#FastAPi modules
from fastapi import APIRouter, Depends, HTTPException, status, Form, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import EmailStr, ValidationError
#SQL ALCHEMY modules
from sqlalchemy.orm import Session
#File System librarys
from pathlib import Path
import shutil
#UID generate (for my image flow)
import uuid
#Models
from app.models.db_user import Users
#Schemas
from app.schemas.usersSchemas import UserRegister, UserLogin, UserResponse, LoginResponse, UserEdit, RegisterResponse, EditResponse, DeleteResponse
#Dependency injection 
from app.database import get_db
#Services (users, hashing, authorization_flow, image flow )
from app.services.usersServices import add_new_user, verified_user, admin_role, user_edit
from app.services.image_services import save_image
#Authorization flow
from app.security.authorization import get_current_user, get_admin
from app.security.hashing import hashed_password

#Personality exepctions
from app.exceptions.userExceptions import AdminRequired, UserNotFound
#Repository
from app.repositories.Users_repositories import UserRepository

#----------------Api config routes--------------------------
#Routes for normal users (Endpoints for users flow)
user = APIRouter(prefix='/user', tags=["User services"])
#Routes for Admin users (Endpoints for user maintain)
user_maintain = APIRouter(prefix='/user_maintain', tags=["User Maintain"])

#Object for my repository (Execute query in my db)
user_tools = UserRepository()

#Path folder for upload image, if not exist it create one
upload_path = Path("uploads")
upload_path.mkdir(exist_ok=True)


#----------User route endpoints--------------------------


#Endpoint for get frontend template in the route "/"
@user.get("/")
async def read_index():
    return FileResponse("index.html")

#Endpoint for get current user using jwt auth
@user.get("/current_user")
def get_actual_user(user = Depends(get_current_user)):
    return user

#Endpoint for register new user
@user.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register_user(username: str = Form(""), age: int = Form(...), email: EmailStr = Form(...), password: str = Form(...), image: UploadFile | None = File(default=None), db: Session = Depends(get_db)):

    try:
        new_user = UserRegister(
            username=username,
            age=age,
            email=email,
            password=password
        )
    except ValidationError as exc:
        raise HTTPException(
            status_code=422,
            detail=[
                {
                    "loc": list(error["loc"]),
                    "msg": error["msg"]
                }
                for error in exc.errors()
            ]
    )

    if image != None:
        image_uid = await save_image(image, new_user.id)

        new_user = add_new_user(new_user, image_uid, db)
        if new_user:
            return {
                "message": "User created successfully",
                "data": new_user
            }

    else:
        new_user = add_new_user(new_user, "profile.png", db)
        if new_user:
            return {
                "message": "User created successfully",
                "data": new_user
            }

#Endpoint for authenthicate user
@user.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login_user(data: UserLogin, db: Session = Depends(get_db)):
    token = verified_user(data, db)
    return token

#------------ User_maintain routes (only admin role) ---------------------

#Get all users from db
@user_maintain.get("/get_users", response_model=list[UserResponse])
def get_users(Admin = Depends(get_admin), db: Session = Depends(get_db)):
        return user_tools.get_users(db)
        


#Get a specific user from db
@user_maintain.post("/get_user", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_tools.found_user_by_id(user_id, db)
   
   


#Edit an exist user 
@user_maintain.put("/edit_user", response_model=EditResponse)
async def edit_user(userId: int = Form(...), new_username: str = Form(...), new_age: int = Form(...), new_email: EmailStr = Form(...), new_password: str = Form(...), new_image: UploadFile = File(default=None), Admin = Depends(get_admin), db: Session = Depends(get_db)):
        older_user = user_tools.found_user_by_id(userId, db)
        if older_user:
            older_image = older_user.image
            try:
                new_user = UserRegister(
                    username=new_username,
                    age=new_age,
                    email=new_email,
                    password=new_password
                )
            except ValidationError as exc:
                raise HTTPException(
                    status_code=422,
                    detail=[
                        {
                            "loc": list(error["loc"]),
                            "msg": error["msg"]
                        }
                        for error in exc.errors()
                    ]
            )
            

            if new_image != None:
                image_uid = await save_image(new_image, older_image)
                user_edited = user_edit(new_user, older_user, image_uid, db)
                if user_edited:
                    return {
                        "message": "User edited successfully",
                        "data": user_edited
                    }

            else:
                user_edited = user_edit(new_user, older_user, older_image, db)
                if user_edited:
                    return {
                        "message": "User edited successfully",
                        "data": user_edited
                    }
        raise UserNotFound()

#delete an exist user
@user_maintain.delete("/delete_user", response_model=DeleteResponse)
def delete_user(id: int, Admin = Depends(get_admin), db: Session = Depends(get_db)):
        user = user_tools.found_user_by_id(id, db)
        if user:
            user_tools.delete_user(user, db)
            return {
                "message": "User deleted successfully",
                "data": user
            }
        raise HTTPException(status_code=404, detail="User was not found")
       
#User for get admin role
@user_maintain.post("/get_admin")
def get_admin_role(id: int, db: Session = Depends(get_db)):
    return admin_role(id, db)



