from pydantic import BaseModel, EmailStr

from models import RoleTypes


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: RoleTypes = RoleTypes.REGULAR_USER


class LoginRequest(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: int
    name: str
    email: EmailStr


class UserUpdate(BaseModel):
    name: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
