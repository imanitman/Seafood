from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from Models.Base import Base

class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    shipper = Column(String)
    status = Column(Enum("PENDING", "PICKED_UP", "IN_TRANSIT", "DELIVERED", "CANCELLED", name="shipment_status_enum"))
    position = Column(String)
    
    order = relationship("Order", back_populates="shipment")