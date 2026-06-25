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
