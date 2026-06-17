from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from Core.database import get_db
from Core.security import hash_password, verify_password, create_token
from schemas.auth import LoginRequest
from Models.User import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(data, db: Session = Depends(get_db)):
    user = User(
        username=data.username,
        email=data.email,
        password=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    return {"message": "registered"}


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = (
        db.query(User)
        .filter(User.username == data.username)
        .first()
    )

    if not user:
        return {"error": "invalid credentials"}

    if not verify_password(
            data.password,
            user.password
    ):
        return {"error": "invalid credentials"}

    token = create_token({
        "user_id": user.id,
        "email": user.email,
        "role": user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }