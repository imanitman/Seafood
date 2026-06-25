from pydantic import BaseModel

class ImageProductSchema(BaseModel):
    product_detail_id: int
    image_url: str
