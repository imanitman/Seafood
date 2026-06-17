from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Core.database import get_db
from Core.security import get_current_user

from Models.CartItem import CartItem
from Models.Product import Product

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/add")
def add_to_cart(
    product_id: int,
    quantity: int = 1,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # check nếu đã có trong cart
    cart_item = db.query(CartItem).filter(
        CartItem.user_id == current_user["user_id"],
        CartItem.product_id == product_id
    ).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            user_id=current_user["user_id"],
            product_id=product_id,
            quantity=quantity
        )
        db.add(cart_item)

    db.commit()

    return {"message": "added to cart"}

@router.get("/")
def get_cart(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    cart_items = db.query(CartItem).filter(
        CartItem.user_id == current_user["user_id"]
    ).all()

    return cart_items

@router.put("/update")
def update_quantity(
    product_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    cart_item = db.query(CartItem).filter(
        CartItem.user_id == current_user["user_id"],
        CartItem.product_id == product_id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not in cart")

    if quantity <= 0:
        db.delete(cart_item)
    else:
        cart_item.quantity = quantity

    db.commit()

    return {"message": "updated"}

@router.delete("/remove")
def remove_from_cart(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    cart_item = db.query(CartItem).filter(
        CartItem.user_id == current_user["user_id"],
        CartItem.product_id == product_id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(cart_item)
    db.commit()

    return {"message": "removed"}

@router.delete("/clear")
def clear_cart(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db.query(CartItem).filter(
        CartItem.user_id == current_user["user_id"]
    ).delete()

    db.commit()

    return {"message": "cart cleared"}