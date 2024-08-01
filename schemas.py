from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


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
