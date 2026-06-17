from sqlalchemy import Column, Integer, String
from Models.Base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))
    role = Column(String(20), default="USER")