#Fastapi modules
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form, File
#Librarys for interact with filesystem
from pathlib import Path
import shutil
#Library for generate UID
import uuid
#SQLALCHEMY And Models
from app.models.db_travels import Travels
from sqlalchemy.orm import Session
#Dependency injection
from app.database import get_db
#Schemas
from app.schemas.travelSchemas import CreateTravel, TravelEdit, Reserve
#Services and repository
from app.services.travelServices import create_travel, travel_edit
from app.repositories.Travels_repositories import TravelRepository
from app.services.booking_services import reserve_travel 

#Auth flow and exceptions handle
from app.security.authorization import get_current_user, get_admin
from app.exceptions.userExceptions import AdminRequired






#Api config for travels 

#Travels route for public services
travels = APIRouter(prefix="/travel", tags=["Travels Service"])
#Travels route for travel maintain services(only admin role)
travels_maintain = APIRouter(prefix="/travel_maintain", tags=["Travels Maintain"])


#travel repository for execute querys in the db
travel_repository = TravelRepository()

#Create a path object and if not exist create uploads folder
upload_dir = Path("uploads")
upload_dir.mkdir(exist_ok=True)

#------------- Travels endpoints (public services) ---------------------

#Endpoint for create a new travel in db
@travels.post("/create_travel")
async def new_travel(destination: str = Form(...), activity: str = Form(...) , price: int = Form(...), available_seats: int = Form(...), duration: int = Form(...), image: UploadFile = File(...), admin = Depends(get_admin) , db: Session = Depends(get_db)):
    #Verify size of the file
    if admin:
        max_size = 5 + (1024 * 1024)
        size = await image.read()
        if len(size) > max_size:
            raise HTTPException(
                status_code=413,
                detail="File too large"
            )
        #Extract suffix of file and restrict 3 types of suffix
        extension = Path(image.filename).suffix
        if extension not in [".jpg", ".png", ".jpeg"]:
            raise HTTPException(
                status_code=400,
                detail="Format supported is (.jpg, .jpeg, .png)"
            )
        #Generate file name
        image_uid = f"{uuid.uuid4()}{extension}"
        #Generate path of the file
        file_path = upload_dir / image_uid

        #Reset cursor inside image bytes
        await image.seek(0)

        #Open file as buffer with "write" and "bytes" permissions, for modify it, then copy content in image inside our buffer object
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

       

        travel_data = CreateTravel(
            destination=destination,
            activity=activity,
            price=price,
            available_seats=available_seats,
            duration=duration
        )

        return create_travel(travel_data, image_uid, db)
    raise AdminRequired()

#Endpoint for reserve a travel
@travels.post("/reserve_travel")
def Reserve_Travel(data:Reserve, user_id = Depends(get_current_user), db: Session = Depends(get_db)):
        booking = reserve_travel(data, db, user_id["user_id"])
        return booking

#Endpoint for get all travels
@travels.get("/get_travels")
def get_travels(db: Session = Depends(get_db)):
    travels = db.query(Travels).all()
    return travels

#--------------Travels maintain routes (Admin only) ----------------

#Get a specific travel in db
@travels_maintain.post("/get_travel")
def get_travel(travel_id: int, admin = Depends(AdminRequired), db: Session = Depends(get_db)):
    if admin:
        return db.query(Travels).filter(Travels.id == travel_id).first()
            


#Edit a travel
@travels_maintain.put("/edit_travel")
def edit_travel(data: TravelEdit, Admin = Depends(get_admin), db: Session = Depends(get_db)):
    if Admin:
        travel = travel_edit(data, db)
        return travel
    raise AdminRequired()


#Delete a travel
@travels_maintain.delete("/delete_travel")
def delete_travel(id: int, Admin = Depends(get_admin), db: Session = Depends(get_db)):
    if Admin:
        travel = TravelRepository.search_travel_by_id(id, db)
        if travel:
            db.delete(travel)
            db.commit()

            return travel
        raise HTTPException(status_code=404, detail="Travel was not found")
    raise AdminRequired()
    

