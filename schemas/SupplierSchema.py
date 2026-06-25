from pydantic import BaseModel
from typing import Optional

class SupplierSchema(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
