from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Core.database import get_db
from Core.security import require_roles
from Models.Payment import Payment

router = APIRouter(prefix="/payments", tags=["payments"])

@router.put("/{payment_id}/status")
def update_payment_status(payment_id: int, status: str, db: Session = Depends(get_db), current_user = Depends(require_roles("ADMIN"))):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    payment.status = status
    db.commit()
    db.refresh(payment)
    return payment
