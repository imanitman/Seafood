import os

from fastapi import FastAPI, APIRouter
from sqlalchemy import text

from api import auth, product, order, category, cart, unit, supplier, product_detail, payment, shipment, image_product, user
from fastapi.middleware.cors import CORSMiddleware
from Models.Base import Base
from Core.database import engine
import Models

Base.metadata.create_all(bind=engine)

with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS unaccent"))
    conn.commit()

# ─────────────────────────────────────────────────────────────────────
# Auto-migration: thêm các cột còn thiếu mà create_all không tự thêm
# ─────────────────────────────────────────────────────────────────────
_ALTER_SQLS = [
    # users
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS phone_number VARCHAR(50)",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS login_method_id INTEGER REFERENCES login_methods(id)",
    # products
    "ALTER TABLE products ADD COLUMN IF NOT EXISTS stock INTEGER",
    "ALTER TABLE products ADD COLUMN IF NOT EXISTS image_url VARCHAR(500)",
    "ALTER TABLE products ADD COLUMN IF NOT EXISTS supplier_id INTEGER REFERENCES suppliers(id)",
    # product_details
    "ALTER TABLE product_details ADD COLUMN IF NOT EXISTS unit_id INTEGER REFERENCES units(id)",
    "ALTER TABLE product_details ADD COLUMN IF NOT EXISTS sales_price INTEGER",
    "ALTER TABLE product_details ADD COLUMN IF NOT EXISTS quantity INTEGER",
    # orders
    "ALTER TABLE orders ADD COLUMN IF NOT EXISTS location_id INTEGER REFERENCES locations(id)",
    # order_items
    "ALTER TABLE order_items ADD COLUMN IF NOT EXISTS product_detail_id INTEGER REFERENCES product_details(id)",
    "ALTER TABLE order_items ADD COLUMN IF NOT EXISTS price FLOAT",
    # cart_items
    "ALTER TABLE cart_items ADD COLUMN IF NOT EXISTS product_detail_id INTEGER REFERENCES product_details(id)",
]

with engine.connect() as conn:
    for sql in _ALTER_SQLS:
        try:
            conn.execute(text(sql))
        except Exception:
            pass  # column already exists or other non-critical error
    conn.commit()
# ─────────────────────────────────────────────────────────────────────

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(product.router)
app.include_router(order.router)
app.include_router(category.router)
app.include_router(cart.router)
app.include_router(unit.router)
app.include_router(supplier.router)
app.include_router(product_detail.router)
app.include_router(payment.router)
app.include_router(shipment.router)
app.include_router(image_product.router)
app.include_router(user.router)

_origins = ["http://localhost:3000"]
_frontend_url = os.getenv("FRONTEND_URL")
if _frontend_url:
    _origins.append(_frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
