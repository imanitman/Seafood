from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from Models.Base import Base

class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    products = relationship("Product", back_populates="unit")   # <-- thêm

    product_details = relationship("ProductDetail", back_populates="unit")