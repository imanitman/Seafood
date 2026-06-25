from pydantic import BaseModel


class CreateLocationRequest(BaseModel):
    address: str
    is_default: bool = False


class LocationResponse(BaseModel):
    id: int
    address: str
    is_default: bool

    class Config:
        from_attributes = True