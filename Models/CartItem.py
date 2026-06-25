from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from Models.Base import Base

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_detail_id = Column(Integer, ForeignKey("product_details.id"))
    quantity = Column(Integer)

    user = relationship("User", back_populates="cart_items")
    product_detail = relationship("ProductDetail", back_populates="cart_items")