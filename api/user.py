from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Core.database import get_db
from Core.security import get_current_user, require_roles
from Models.User import User
from schemas.user import UserUpdateSchema

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
def get_me(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # remove password from response
    user_dict = user.__dict__.copy()
    user_dict.pop("password", None)
    return user_dict

@router.put("/me")
def update_me(request: UserUpdateSchema, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if request.phone_number is not None:
        user.phone_number = request.phone_number
    if request.username is not None:
        user.username = request.username
    if request.email is not None:
        user.email = request.email

    db.commit()
    db.refresh(user)
    
    user_dict = user.__dict__.copy()
    user_dict.pop("password", None)
    return user_dict

@router.get("/")
def get_all_users(db: Session = Depends(get_db), current_user=Depends(require_roles("ADMIN"))):
    users = db.query(User).all()
    results = []
    for u in users:
        u_dict = u.__dict__.copy()
        u_dict.pop("password", None)
        results.append(u_dict)
    return results
