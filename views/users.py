from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import User, UserUpdate
from utils.jwt import get_current_user, admin_required
from models import User as User_model

router = APIRouter(prefix='/users')


@router.get("/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put('/me', response_model=User)
def update_user(user_update: UserUpdate, db: Session = Depends(get_db)):
    pass


@router.get("", response_model=List[User], dependencies=[Depends(admin_required)])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User_model).all()
