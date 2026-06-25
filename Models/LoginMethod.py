from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from Models.Base import Base

class LoginMethod(Base):
    __tablename__ = "login_methods"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)
    
    users = relationship("User", back_populates="login_method")
