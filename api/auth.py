from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from Core.database import get_db
from Core.security import (
    hash_password, verify_password, create_token, get_current_user
)
from schemas.auth import LoginRequest, RegisterRequest
from Models.User import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(
        (User.username == data.username) | (User.email == data.email)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    user = User(
        username=data.username,
        email=data.email,
        password=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    return {"message": "registered"}


@router.post("/login")
def login(data: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({
        "user_id": user.id,
        "email": user.email,
        "role": user.role,
        "username": user.username
    })

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=3600,
        samesite="lax",
        secure=False,
    )
    return {
        "user_id": user.id,
        "email": user.email,
        "role": user.role,
        "username": user.username
    }


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token", samesite="lax")
    return {"message": "logged out"}


@router.get("/me")
def me(current_user=Depends(get_current_user)):
    return current_user
