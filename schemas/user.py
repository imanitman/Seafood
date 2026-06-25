from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

from typing import Optional

class UserUpdateSchema(BaseModel):
    phone_number: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None