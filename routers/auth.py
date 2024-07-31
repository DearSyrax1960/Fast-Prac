from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas.user import UserCreate, UserOut

router = APIRouter(prefix='/auth')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post('/signup', response_model=UserOut)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    check_existing_user(user.username, user.email, db)

    hashed_password = hash_password(user.password)

    new_user = create_user(user.username, user.email, hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def check_existing_user(username: str, email: str, db: Session):
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="Username already exists.")
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered.")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_user(username: str, email: str, hashed_password: str) -> User:
    return User(username=username, email=email, password=hashed_password)
