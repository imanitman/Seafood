from pydantic import BaseModel
from typing import Optional


class ProductSchema(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category_id: int
    image_url: Optional[str] = None