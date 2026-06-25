from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from Models.Base import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    
    products = relationship("Product", back_populates="category")