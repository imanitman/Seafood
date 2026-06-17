from sqlalchemy import Column, Integer, Float, String, ForeignKey
from Models.Base import Base 

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_price = Column(Float)
    status = Column(String(50), default="PENDING")