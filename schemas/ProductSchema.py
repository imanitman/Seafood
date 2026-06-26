from pydantic import BaseModel
from typing import Optional

class ProductSchema(BaseModel):
    name: str
    description: str
    price: float
    stock: int

    category_id: int
    unit_id: int                  # <-- thêm

    supplier_id: Optional[int] = None
    image_url: Optional[str] = None