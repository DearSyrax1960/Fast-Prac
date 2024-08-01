from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import User, UserUpdate
from utils.jwt import get_current_user

router = APIRouter(prefix='/users')


@router.get("/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user



