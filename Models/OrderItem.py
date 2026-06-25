from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from Models.Base import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_detail_id = Column(Integer, ForeignKey("product_details.id"))
    quantity = Column(Integer)
    price = Column(Float)
    
    order = relationship("Order", back_populates="order_items")
    product_detail = relationship("ProductDetail", back_populates="order_items")