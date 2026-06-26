from fastapi import HTTPException
import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, UploadFile, File, Depends
from Core.config import (
    CLOUDINARY_CLOUD_NAME,
    CLOUDINARY_API_KEY,
    CLOUDINARY_API_SECRET,
)

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True,
)
from sqlalchemy.orm import joinedload
from Core.security import require_roles
from schemas.ProductSchema import ProductSchema
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import asc, desc, func, or_
from sqlalchemy.orm import Session
from Core.database import get_db
from Models.Product import Product
from Models.OrderItem import OrderItem


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
    query = (
        db.query(Product)
        .options(
            joinedload(Product.category),
            joinedload(Product.supplier),
            joinedload(Product.unit)
        )
    )

    # Search
    if search:
        for word in search.strip().split():
            pattern = f"%{word}%"
            query = query.filter(
                or_(
                    func.unaccent(Product.name).ilike(func.unaccent(pattern)),
                    func.unaccent(Product.description).ilike(func.unaccent(pattern))
                )
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

@router.get("/bestsellers")
def get_bestsellers(
    limit: int = 8,
    db: Session = Depends(get_db)
):
    from Models.ProductDetail import ProductDetail
    results = (
        db.query(Product, func.sum(OrderItem.quantity).label("total_sold"))
        .join(ProductDetail, ProductDetail.product_id == Product.id)
        .join(OrderItem, OrderItem.product_detail_id == ProductDetail.id)
        .group_by(Product.id)
        .order_by(desc(func.sum(OrderItem.quantity)))
        .limit(limit)
        .all()
    )
    return [r[0] for r in results]


#lay product theo id
@router.get("/{product_id}")
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
        product = (
            db.query(Product)
            .options(
                joinedload(Product.product_details),
                joinedload(Product.category),
                joinedload(Product.supplier),
                joinedload(Product.unit)
            )
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
    db: Session = Depends(get_db),
    current_user = Depends(require_roles("ADMIN"))
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
    db: Session = Depends(get_db),
    current_user = Depends(require_roles("ADMIN"))
):
        product = Product(
            name=request.name,
            description=request.description,
            price=request.price,
            stock=request.stock,
            category_id=request.category_id,
            supplier_id=request.supplier_id,
            unit_id=request.unit_id,
            image_url=request.image_url
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
    current_user = Depends(require_roles("ADMIN")),
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
    product.supplier_id = request.supplier_id
    product.image_url = request.image_url

    db.commit()
    db.refresh(product)

    return product


@router.get("/{category_id}/products")
def get_products_by_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    return db.query(Product)\
        .filter(Product.category_id == category_id)\
        .all()


@router.post("/fix-image-urls")
def fix_image_urls(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("ADMIN"))
):
    default_url = "https://res.cloudinary.com/diblzcbla/image/upload/products/default.jpg"
    bad_prefix = "http://localhost:8000"
    products = db.query(Product).filter(
        Product.image_url.like(f"{bad_prefix}%")
    ).all()
    fixed = []
    for p in products:
        p.image_url = default_url
        fixed.append({"id": p.id, "image_url": p.image_url})
    db.commit()
    return {"fixed": len(fixed), "items": fixed}

@router.put("/{product_id}")
def update_product(
    product_id: int,
    request: ProductSchema,
    current_user=Depends(require_roles("ADMIN")),
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
    product.supplier_id = request.supplier_id
    product.unit_id = request.unit_id
    product.image_url = request.image_url

    db.commit()
    db.refresh(product)

    return product

@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    current_user=Depends(require_roles("ADMIN"))
):
    contents = await file.read()
    try:
        result = cloudinary.uploader.upload(
            contents,
            folder="products",
            resource_type="image",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cloudinary upload failed: {str(e)}")
    url = result["secure_url"]
    filename = result["public_id"].split("/")[-1]
    return {
        "filename": filename,
        "url": url,
    }