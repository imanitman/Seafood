from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Core.database import get_db
from Core.security import require_roles, get_current_user

from Models.Order import Order
from Models.OrderItem import OrderItem
from Models.CartItem import CartItem
from Models.ProductDetail import ProductDetail
from Models.Payment import Payment
from Models.Shipment import Shipment
from Models.Location import Location

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)
@router.post("/")
def create_order(
    location_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = current_user["user_id"]

    location = db.query(Location).filter(Location.id == location_id, Location.user_id == user_id).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    from sqlalchemy.orm import joinedload
    cart_items = (
        db.query(CartItem)
        .options(joinedload(CartItem.product_detail))
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
        price_to_use = item.product_detail.sales_price if item.product_detail.sales_price else item.product_detail.price
        total_price += (
            price_to_use * item.quantity
        )

    order = Order(
        user_id=user_id,
        location_id=location_id,
        total_price=total_price,
        status="PENDING"
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    payment = Payment(
        order_id=order.id,
        payment_method="CASH",
        amount=total_price,
        status="PENDING"
    )
    db.add(payment)

    shipment = Shipment(
        order_id=order.id,
        shipper="",
        status="PENDING",
        position=""
    )
    db.add(shipment)
    db.commit()

    for item in cart_items:
        price_to_use = item.product_detail.sales_price if item.product_detail.sales_price else item.product_detail.price
        order_item = OrderItem(
            order_id=order.id,
            product_detail_id=item.product_detail_id,
            quantity=item.quantity,
            price=price_to_use
        )

        db.add(order_item)

        product_detail = (
            db.query(ProductDetail)
            .filter(
                ProductDetail.id == item.product_detail_id
            )
            .first()
        )

        product_detail.quantity -= item.quantity

    db.commit()

    db.query(CartItem).filter(
        CartItem.user_id == user_id
    ).delete()

    db.commit()

    return order

@router.get("/")
def get_orders(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = current_user["user_id"]
    from sqlalchemy.orm import joinedload
    return (
        db.query(Order)
        .options(joinedload(Order.payment), joinedload(Order.shipment))
        .filter(Order.user_id == user_id)
        .all()
    )

@router.get("/{order_id}")
def get_order_detail(
    order_id: int,
    db: Session = Depends(get_db)
):
    from sqlalchemy.orm import joinedload
    order = (
        db.query(Order)
        .options(joinedload(Order.payment), joinedload(Order.shipment))
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
        .options(joinedload(OrderItem.product_detail))
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
    from sqlalchemy.orm import joinedload
    return db.query(Order).options(joinedload(Order.payment), joinedload(Order.shipment)).all()

@router.put("/{order_id}/status")
def update_status(
    order_id: int,
    status: str,
    current_user = Depends(require_roles("ADMIN")),
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