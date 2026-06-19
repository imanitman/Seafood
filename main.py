from fastapi import FastAPI, APIRouter
from sqlalchemy import text

from api import auth, product, order, category, cart
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
