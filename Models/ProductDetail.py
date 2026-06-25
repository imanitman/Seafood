from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from Models.Base import Base

class ProductDetail(Base):
    __tablename__ = "product_details"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    unit_id = Column(Integer, ForeignKey("units.id"))
    description = Column(Text)
    price = Column(Integer)
    sales_price = Column(Integer)
    quantity = Column(Integer)
    
    product = relationship("Product", back_populates="product_details")
    unit = relationship("Unit", back_populates="product_details")
    images = relationship("ImageProduct", back_populates="product_detail")
    order_items = relationship("OrderItem", back_populates="product_detail")
    cart_items = relationship("CartItem", back_populates="product_detail")