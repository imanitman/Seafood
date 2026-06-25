from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Core.database import get_db
from Core.security import require_roles
from Models.Supplier import Supplier
from schemas.SupplierSchema import SupplierSchema

router = APIRouter(prefix="/suppliers", tags=["suppliers"])

@router.get("/")
def get_suppliers(db: Session = Depends(get_db)):
    return db.query(Supplier).all()

@router.post("/")
def create_supplier(request: SupplierSchema, db: Session = Depends(get_db), current_user = Depends(require_roles("ADMIN"))):
    supplier = Supplier(
        name=request.name,
        phone=request.phone,
        email=request.email,
        address=request.address
    )
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier

@router.delete("/{supplier_id}")
def delete_supplier(supplier_id: int, db: Session = Depends(get_db), current_user = Depends(require_roles("ADMIN"))):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    db.delete(supplier)
    db.commit()
    return {"message": "Supplier deleted"}
