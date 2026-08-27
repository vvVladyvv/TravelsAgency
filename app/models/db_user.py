from sqlalchemy import Integer, String, Column, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String[255], nullable=False)
    age = Column(Integer, CheckConstraint('age >= 18'), nullable=False)
    email = Column(String[255], unique=True, nullable=False)
    password = Column(String[255], nullable=False)
    role = Column(String, server_default="user", nullable=False)
    image = Column(String, server_default="user.png", nullable=True)

    booking = relationship("Bookings", back_populates="user")


    