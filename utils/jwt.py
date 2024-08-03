import os
import time

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, ExpiredSignatureError, JWTError
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from dependencies import get_db
from schemas.token_schema import TokenData
from utils.repo import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = time.time() + ACCESS_TOKEN_EXPIRE_MINUTES * 60
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    email: str = decode_token(token).get("sub")
    if email is None:
        raise credentials_exception
    token_data = TokenData(username=email)
    user = get_user_by_email(db, email=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def admin_required(token: str = Depends(oauth2_scheme)):
    role: str = decode_token(token=token).get("role")
    if role is None:
        raise credentials_exception
    if role != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not enough permissions")


def decode_token(token: str) -> dict:
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="token has been expired you have to login. ")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=" invalid token")
    return payload
