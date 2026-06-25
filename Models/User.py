from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from Models.Base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    phone_number = Column(String)
    username = Column(String(100), unique=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))
    role = Column(String(20), default="USER")
    
    login_method_id = Column(Integer, ForeignKey("login_methods.id"))
    
    login_method = relationship("LoginMethod", back_populates="users")
    locations = relationship("Location", back_populates="user")
    orders = relationship("Order", back_populates="user")
    cart_items = relationship("CartItem", back_populates="user")