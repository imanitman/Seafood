from pydantic import BaseModel
from typing import Optional

class ProductDetailSchema(BaseModel):
    product_id: int
    unit_id: int
    description: Optional[str] = None
    price: int
    sales_price: Optional[int] = None
    quantity: int
