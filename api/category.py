from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Core.database import get_db
from Models.Category import Category

router = APIRouter(prefix="/categories", tags=["categories"])

@router.post("/")
def create_category(name: str, db: Session = Depends(get_db)):
    existing = db.query(Category).filter(Category.name == name).first()

    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")

    category = Category(name=name)

    db.add(category)
    db.commit()
    db.refresh(category)

    return category

@router.get("/")
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.get("/{category_id}")
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return category

@router.put("/{category_id}")
def update_category(
    category_id: int,
    name: str,
    db: Session = Depends(get_db)
):
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    category.name = name

    db.commit()
    db.refresh(category)

    return category

@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()

    return {"message": "deleted successfully"}