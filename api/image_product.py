from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Core.database import get_db
from Core.security import require_roles
from Models.ImageProduct import ImageProduct
from schemas.ImageProductSchema import ImageProductSchema

router = APIRouter(prefix="/image-products", tags=["image_products"])

@router.post("/")
def create_image_product(request: ImageProductSchema, db: Session = Depends(get_db), current_user = Depends(require_roles("ADMIN"))):
    image = ImageProduct(
        product_detail_id=request.product_detail_id,
        image_url=request.image_url
    )
    db.add(image)
    db.commit()
    db.refresh(image)
    return image

@router.delete("/{image_id}")
def delete_image_product(image_id: int, db: Session = Depends(get_db), current_user = Depends(require_roles("ADMIN"))):
    image = db.query(ImageProduct).filter(ImageProduct.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    db.delete(image)
    db.commit()
    return {"message": "Image deleted"}
