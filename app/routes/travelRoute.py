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
from app.repositories.Travels_repositories import TravelRepository



travel_repository = TravelRepository()
travels = APIRouter(prefix="/travel", tags=["Travels Service"])
travels_maintain = APIRouter(prefix="/travel_maintain", tags=["Travels Maintain"])


#Create a path object and if not exist create uploads folder
upload_dir = Path("uploads")
upload_dir.mkdir(exist_ok=True)

#Learn this-------------------------------
@travels.post("/create_travel")
async def new_travel(destination: str = Form(...), activity: str = Form(...) , price: int = Form(...), available_seats: int = Form(...), duration: int = Form(...), image: UploadFile = File(...), admin = Depends(get_admin) , db: Session = Depends(get_db)):
    if admin:
        max_size = 5 + (1024 * 1024)
        size = await image.read()
        if len(size) > max_size:
            raise HTTPException(
                status_code=413,
                detail="File too large"
            )
        #FIrst extract extension from the file and then generate and uuid and mix it with our extension
        extension = Path(image.filename).suffix
        if extension not in [".jpg", ".png", ".jpeg"]:
            raise HTTPException(
                status_code=400,
                detail="Format supported is (.jpg, .jpeg, .png)"
            )
        unique_name = f"{uuid.uuid4()}{extension}"

        #Create a file path for can access
        file_path = upload_dir / unique_name



        #then we open the content with "wb" paremeters for can write in binary mode
        with file_path.open("wb") as buffer:
            #Extract the binary code inside our upload image, and paste it inside our new image
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

@travels_maintain.post("/get_travel")
def get_travel(travel_id: int, admin = Depends(AdminRequired), db: Session = Depends(get_db)):
    if admin:
        return db.query(Travels).filter(Travels.id == travel_id).first()
            



@travels_maintain.put("/edit_travel")
def edit_travel(data: TravelEdit, Admin = Depends(get_admin), db: Session = Depends(get_db)):
    if Admin:
        travel = travel_edit(data, db)
        return travel
    raise AdminRequired()

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
    

