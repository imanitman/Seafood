from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Core.database import get_db
from Core.security import require_roles

from Models.Order import Order
from Models.OrderItem import OrderItem
from Models.CartItem import CartItem
from Models.Product import Product

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)
@router.post("/")
def create_order(
    user_id: int,
    db: Session = Depends(get_db)
):
    cart_items = (
        db.query(CartItem)
        .filter(CartItem.user_id == user_id)
        .all()
    )

    if not cart_items:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty"
        )

    total_price = 0

    for item in cart_items:
        total_price += (
            item.product.price * item.quantity
        )

    order = Order(
        user_id=user_id,
        total_price=total_price,
        status="PENDING"
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price
        )

        db.add(order_item)

        product = (
            db.query(Product)
            .filter(
                Product.id == item.product_id
            )
            .first()
        )

        product.stock -= item.quantity

    db.commit()

    db.query(CartItem).filter(
        CartItem.user_id == user_id
    ).delete()

    db.commit()

    return order

@router.get("/")
def get_orders(
    user_id: int,
    db: Session = Depends(get_db)
):
    return (
        db.query(Order)
        .filter(Order.user_id == user_id)
        .all()
    )

@router.get("/{order_id}")
def get_order_detail(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    items = (
        db.query(OrderItem)
        .filter(
            OrderItem.order_id == order_id
        )
        .all()
    )

    return {
        "order": order,
        "items": items
    }

@router.put("/{order_id}/cancel")
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    order.status = "CANCELLED"

    db.commit()

    return {
        "message": "Order cancelled"
    }

@router.get("/admin/all")
def get_all_orders(
    db: Session = Depends(get_db)
):
    return db.query(Order).all()

@router.put("/{order_id}/status")
def update_status(
    order_id: int,
    status: str,
    current_user = Depends(require_roles),
    db: Session = Depends(get_db),

):
    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    order.status = status

    db.commit()

    return order