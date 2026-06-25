from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Core.database import get_db
from Core.security import require_roles
from Models.ProductDetail import ProductDetail
from schemas.ProductDetailSchema import ProductDetailSchema

router = APIRouter(prefix="/product-details", tags=["product_details"])

@router.post("/")
def create_product_detail(request: ProductDetailSchema, db: Session = Depends(get_db), current_user = Depends(require_roles("ADMIN"))):
    detail = ProductDetail(
        product_id=request.product_id,
        unit_id=request.unit_id,
        description=request.description,
        price=request.price,
        sales_price=request.sales_price,
        quantity=request.quantity
    )
    db.add(detail)
    db.commit()
    db.refresh(detail)
    return detail

@router.delete("/{detail_id}")
def delete_product_detail(detail_id: int, db: Session = Depends(get_db), current_user = Depends(require_roles("ADMIN"))):
    detail = db.query(ProductDetail).filter(ProductDetail.id == detail_id).first()
    if not detail:
        raise HTTPException(status_code=404, detail="Product Detail not found")
    db.delete(detail)
    db.commit()
    return {"message": "Product Detail deleted"}
