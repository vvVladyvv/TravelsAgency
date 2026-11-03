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
from app.schemas.travelSchemas import CreateTravel, Reserve
#Services and repository
from app.services.travelServices import create_travel, travel_edit, get_tendences
from app.repositories.Travels_repositories import TravelRepository
from app.services.booking_services import reserve_travel
from app.services.image_services import save_image

#Auth flow and exceptions handle
from app.security.authorization import get_current_user, get_admin
from app.exceptions.userExceptions import AdminRequired
from app.exceptions.travelsExceptions import TravelNotFound






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

    try:
        travel_data = CreateTravel(
            destination=destination,
            activity=activity,
            price=price,
            available_seats=available_seats,
            duration=duration,
            image=image
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

    image_uid = save_image(image)
    return create_travel(travel_data, image_uid, db)

#Endpoint for reserve a travel
@travels.post("/reserve_travel", status_code=201)
def Reserve_Travel(data:Reserve, user_id = Depends(get_current_user), db: Session = Depends(get_db)):
        booking = reserve_travel(data, db, user_id["user_id"])
        return booking

#Endpoint for get all travels
@travels.get("/get_travels")
def get_travels(db: Session = Depends(get_db)):
    return travel_repository.get_all_travels(db)

@travels.get("/tendence_travels")
def travels_tendences(db: Session = Depends(get_db)):
    travels = get_tendences(db)
    return travels

#--------------Travels maintain routes (Admin only) ----------------

#Get a specific travel in db
@travels_maintain.post("/get_travel")
def get_travel(travel_id: int, admin = Depends(AdminRequired), db: Session = Depends(get_db)):
    return travel_repository.search_travel_by_id(travel_id, db)
            


#Edit a travel
@travels_maintain.put("/edit_travel")
async def edit_travel(travelId: int = Form(...), destination: str = Form(...), activity: str = Form(...), price: float = Form(...), available_seats: int = Form(...), duration: int = Form(...), image: UploadFile = File(...), Admin = Depends(get_admin), db: Session = Depends(get_db)):
    try:
        travel_Data = CreateTravel(
            destination=destination,
            activity=activity,
            price=price,
            available_seats=available_seats,
            duration=duration
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
    

    image_file = await save_image(image)
    return travel_edit(travelId, travel_Data, image_file, db)
       


#Delete a travel
@travels_maintain.delete("/delete_travel")
def delete_travel(id: int, Admin = Depends(get_admin), db: Session = Depends(get_db)):
        travel = TravelRepository.search_travel_by_id(id, db)
        if travel:
            return travel_repository.delete_travel(travel, db)
        raise TravelNotFound()

