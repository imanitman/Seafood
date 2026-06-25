from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from Models.Base import Base

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    address = Column(String)
    is_default = Column(Boolean)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="locations")
    orders = relationship("Order", back_populates="location")
