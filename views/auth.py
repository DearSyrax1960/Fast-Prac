from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from utils import repo
from models import User
from schemas import Token, UserCreate
from utils.jwt import create_access_token, authenticate_user
from utils.password import get_password_hash

router = APIRouter(prefix='/auth')


@router.post('/signup', response_model=Token)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    if not repo.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered.")

    hashed_password = get_password_hash(user.password)

    new_user = User(name=user.name, email=user.email, password=hashed_password)
    repo.save_user(db, new_user)

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
