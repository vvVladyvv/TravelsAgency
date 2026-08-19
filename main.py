from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from app.models import db_booking, db_user, db_travels
from app.routes import travelRoute
from app.routes import usersRoute
from app.database import Base, engine



app = FastAPI()


Base.metadata.create_all(bind=engine)

app.include_router(usersRoute.user)
app.include_router(usersRoute.user_maintain)


app.include_router(travelRoute.travels)
app.include_router(travelRoute.travels_maintain)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")



