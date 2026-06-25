from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Core.database import get_db
from Core.security import require_roles
from Models.Unit import Unit
from schemas.UnitSchema import UnitSchema

router = APIRouter(prefix="/units", tags=["units"])

@router.get("/")
def get_units(db: Session = Depends(get_db)):
    return db.query(Unit).all()

@router.post("/")
def create_unit(request: UnitSchema, db: Session = Depends(get_db), current_user = Depends(require_roles("ADMIN"))):
    unit = Unit(name=request.name)
    db.add(unit)
    db.commit()
    db.refresh(unit)
    return unit

@router.delete("/{unit_id}")
def delete_unit(unit_id: int, db: Session = Depends(get_db), current_user = Depends(require_roles("ADMIN"))):
    unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    db.delete(unit)
    db.commit()
    return {"message": "Unit deleted"}
