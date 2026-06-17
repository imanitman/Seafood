from fastapi import FastAPI, APIRouter

from api import auth, product, order

from Models.Base import Base
from Core.database import engine
import Models

Base.metadata.create_all(bind=engine)

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(product.router)
app.include_router(order.router)