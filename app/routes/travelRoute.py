from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form, File
#learn this-----------------
from pathlib import Path
import shutil
import uuid
#-----------------
from app.models.db_travels import Travels
from app.schemas.travelSchemas import CreateTravel, TravelEdit, Reserve
from sqlalchemy.orm import Session
from app.database import get_db
from app.security.authorization import get_current_user, get_admin
from app.services.travelServices import create_travel, travel_edit
from app.services.booking_services import reserve_travel 
from app.exceptions.userExceptions import AdminRequired
from app.repositories.Users_repositories import UserRepository



user_repository = UserRepository()
travels = APIRouter(prefix="/travel", tags=["Travels Service"])
travels_maintain = APIRouter(prefix="/travel_maintain", tags=["Travels Maintain"])

upload_dir = Path("uploads")
upload_dir.mkdir(exist_ok=True)

#Learn this-------------------------------
@travels.post("/create_travel")
def new_travel(destination: str = Form(...), activity: str = Form(...) , price: int = Form(...), available_seats: int = Form(...), duration: int = Form(...), image: UploadFile = File(...), Admin = Depends(get_admin), db: Session = Depends(get_db)):
    if Admin:
        file_path = upload_dir / image.filename

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        travel_data = CreateTravel(
            destination=destination,
            activity=activity,
            price=price,
            available_seats=available_seats,
            duration=duration
        )

        return create_travel(travel_data, image.filename, db)
    raise AdminRequired()
#-----------------------------------------------

@travels.post("/reserve_travel")
def Reserve_Travel(data:Reserve, user_id = Depends(get_current_user), db: Session = Depends(get_db)):
        booking = reserve_travel(data, db, user_id["user_id"])
        return booking


@travels_maintain.get("/get_travels")
def get_travels(db: Session = Depends(get_db)):
    travels = db.query(Travels).all()
    return travels
    




@travels_maintain.put("/edit_travel")
def edit_user(data: TravelEdit, Admin = Depends(get_admin), db: Session = Depends(get_db)):
    if Admin:
        user = travel_edit(data, db)
        return user
    raise AdminRequired()

@travels_maintain.delete("/delete_travel")
def delete_user(id: int, Admin = Depends(get_admin), db: Session = Depends(get_db)):
    if Admin:
        user = user_repository.found_user_by_id(id, db)
        if user:
            db.delete(user)
            db.commit()

            return user
        raise HTTPException(status_code=404, detail="User was not found")
    raise AdminRequired()
    

