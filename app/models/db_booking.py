from sqlalchemy import Integer, String, Column, Numeric, ForeignKey, Boolean
from app.database import Base
from sqlalchemy.orm import relationship

class Bookings(Base):
    __tablename__ = "bookings"
    id = Column(Integer, autoincrement=True, primary_key=True)
    travel_id = Column(ForeignKey("travels.id"))
    user_id = Column(ForeignKey("users.id"))
    companions = Column(Integer, default=0)
    food_include = Column(Boolean, default=False)
    status = Column(String, default="pending")
    cost = Column(Numeric(10, 2))

    user = relationship("Users", back_populates="booking")


    
    