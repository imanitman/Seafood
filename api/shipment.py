from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Core.database import get_db
from Core.security import require_roles
from Models.Shipment import Shipment

router = APIRouter(prefix="/shipments", tags=["shipments"])

@router.put("/{shipment_id}/status")
def update_shipment_status(shipment_id: int, status: str, db: Session = Depends(get_db), current_user = Depends(require_roles("ADMIN"))):
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    shipment.status = status
    db.commit()
    db.refresh(shipment)
    return shipment
