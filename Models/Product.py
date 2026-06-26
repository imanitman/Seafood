from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from Models.Base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(1000))
    price = Column(Float)
    stock = Column(Integer)
    image_url = Column(String(500))

    category_id = Column(Integer, ForeignKey("categories.id"))
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    unit_id = Column(Integer, ForeignKey("units.id"))   # <-- thêm

    category = relationship("Category", back_populates="products")
    supplier = relationship("Supplier", back_populates="products")
    unit = relationship("Unit", back_populates="products")   # <-- thêm
    cart_items = relationship(
        "CartItem",
        back_populates="product"
    )
    product_details = relationship("ProductDetail", back_populates="product")