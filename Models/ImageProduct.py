from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from Models.Base import Base

class ImageProduct(Base):
    __tablename__ = "image_products"

    id = Column(Integer, primary_key=True)
    product_detail_id = Column(Integer, ForeignKey("product_details.id"))
    image_url = Column(String)
    
    product_detail = relationship("ProductDetail", back_populates="images")