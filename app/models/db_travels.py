from sqlalchemy import Integer, String, Column, CheckConstraint
from app.database import Base

class Travels(Base):
    __tablename__ = "travels"
    id = Column(Integer, autoincrement=True, primary_key=True)
    destination = Column(String[255], nullable=False)
    activity = Column(String[255], nullable=False)
    price = Column(Integer, CheckConstraint('price > 0'), nullable=False)
    available_seats = Column(Integer,  nullable=False)
    duration = Column(Integer, CheckConstraint('duration > 0'))
    image = Column(String, nullable=True)

