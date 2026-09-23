#FastAPi modules
from fastapi import APIRouter, Depends, HTTPException, status, Form, UploadFile, File
from fastapi.responses import FileResponse
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
from app.schemas.usersSchemas import UserRegister, UserLogin, UserResponse, LoginResponse, UserEdit
#Dependency injection 
from app.database import get_db
#Services (users, hashing, authorization_flow )
from app.services.usersServices import add_new_user, verified_user, admin_role
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
@user.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(username: str = Form(...), age: int = Form(...), email: str = Form(...), password: str = Form(...), image: UploadFile = File(...), db: Session = Depends(get_db)):

    extension = Path(image.filename).suffix
    image_uuid = f"{uuid.uuid4()}{extension}"

    image_path = upload_path / image_uuid

    with image_path.open("wb") as buffer:
        shutil.copyfileobj(image.file, buffer)


    new_user = UserRegister(
        username=username,
        age=age,
        email=email,
        password=password
    )

    user = add_new_user(new_user, image_uuid, db)
    return user

#Endpoint for authenthicate user
@user.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login_user(data: UserLogin, db: Session = Depends(get_db)):
    token = verified_user(data, db)
    return token

#------------ User_maintain routes (only admin role) ---------------------

#Get all users from db
@user_maintain.get("/get_users", response_model=list[UserResponse])
def get_users(Admin = Depends(get_admin), db: Session = Depends(get_db)):
    if Admin:
        user = db.query(Users).all()
        return user
    raise AdminRequired()


#Get a specific user from db
@user_maintain.post("/get_user", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_tools.found_user_by_id(user_id, db)
    return user
   


#Edit an exist user 
@user_maintain.put("/edit_user", response_model=UserResponse)
def edit_user(userId: int = Form(...), new_username: str = Form(...), new_age: int = Form(...), new_email: str = Form(...), new_password: str = Form(...), new_image: UploadFile = File(...), Admin = Depends(get_admin), db: Session = Depends(get_db)):


    if Admin:
        user = user_tools.found_user_by_id(userId, db)
        if user:
            new_user = UserRegister(
                        username=new_username,
                        age=new_age,
                        email=new_email,
                        password=new_password
                    )
            
            older_img_name = user.image
            older_img_path = upload_path / older_img_name

            extension = Path(new_image.filename).suffix
            uuid_image = f"{uuid.uuid4()}{extension}"

            file_path = upload_path / uuid_image
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(new_image.file, buffer)
         
            user.username = new_user.username
            user.age = new_user.age
            user.email = new_user.email
            user.password = hashed_password(new_user.password)
            user.image = uuid_image

            db.commit()
            db.refresh(user)
            return user
        raise UserNotFound()

    raise AdminRequired()


#delete an exist user
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

#User for get admin role
@user_maintain.post("/get_admin")
def get_admin_role(id: int, db: Session = Depends(get_db)):
    return admin_role(id, db)



