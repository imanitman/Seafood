from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from Models.Base import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    payment_method = Column(Enum("CASH", "VNPAY", "MOMO", "PAYPAL", name="payment_method_enum"))
    amount = Column(Integer)
    status = Column(Enum("PENDING", "SUCCESS", "FAILED", name="payment_status_enum"))
    
    order = relationship("Order", back_populates="payment")