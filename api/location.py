from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Core.security import get_current_user

from Core.database import get_db
from Models.Location import Location
from schemas.location import (
    CreateLocationRequest,
    LocationResponse
)

router = APIRouter(
    prefix="/locations",
    tags=["Locations"]
)


@router.post(
    "",
    response_model=LocationResponse
)
def create_location(
    request: CreateLocationRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    location = Location(
        address=request.address,
        is_default=request.is_default,
        user_id=current_user["user_id"]
    )

    db.add(location)
    db.commit()
    db.refresh(location)

    return location