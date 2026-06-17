from pydantic import BaseModel


class ProductSchema(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category_id: int