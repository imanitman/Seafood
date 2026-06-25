from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from Models.Base import Base

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(20))
    email = Column(String(255), unique=True)
    address = Column(String(500))
    
    products = relationship("Product", back_populates="supplier")