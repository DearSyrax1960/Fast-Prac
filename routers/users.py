from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from schemas.user_schema import UserOut, UserUpdate
from utils.jwt import get_current_user, admin_required
from models.users_model import User as User_model

router = APIRouter()


@router.get("/me", response_model=UserOut)
def read_users_me(current_user: UserOut = Depends(get_current_user)):
    return current_user


@router.put('/me', response_model=UserOut)
def update_user(user_update: UserUpdate, db: Session = Depends(get_db),
                current_user: UserOut = Depends(get_current_user)):
    current_user.name = user_update.name
    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("", response_model=List[UserOut], dependencies=[Depends(admin_required)])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User_model).all()
