from http.client import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from Core.database import get_db
from Models.Product import Product
from schemas.ProductSchema import ProductSchema

router = APIRouter(prefix="/products", tags=["products"])


from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from Core.database import get_db
from Models.Product import Product

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

# lay product duoc filter
@router.get("/")
def get_products(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product)

    # Search
    if search:
        query = query.filter(
            Product.name.ilike(f"%{search}%")
        )

    # Filter category
    if category_id:
        query = query.filter(
            Product.category_id == category_id
        )

    # Filter price
    if min_price is not None:
        query = query.filter(
            Product.price >= min_price
        )

    if max_price is not None:
        query = query.filter(
            Product.price <= max_price
        )

    # Sort
    if sort == "price_asc":
        query = query.order_by(
            asc(Product.price)
        )

    elif sort == "price_desc":
        query = query.order_by(
            desc(Product.price)
        )

    elif sort == "newest":
        query = query.order_by(
            desc(Product.id)
        )

    total = query.count()

    products = (
        query
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )

    return {
        "page": page,
        "size": size,
        "total": total,
        "items": products
    }

#lay product theo id
@router.get("/{product_id}")
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product

#xoa product
@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Deleted successfully"
    }


#them product
@router.post("/")
def create_product(
    request: ProductSchema,
    db: Session = Depends(get_db)
):
    product = Product(
        name=request.name,
        description=request.description,
        price=request.price,
        stock=request.stock,
        category_id=request.category_id
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product

#cap nhat product
@router.put("/{product_id}")
def update_product(
    product_id: int,
    request: ProductSchema,
    db: Session = Depends(get_db)
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product.name = request.name
    product.description = request.description
    product.price = request.price
    product.stock = request.stock
    product.category_id = request.category_id

    db.commit()
    db.refresh(product)

    return product