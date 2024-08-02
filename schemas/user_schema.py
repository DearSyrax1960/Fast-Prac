from pydantic import BaseModel, EmailStr

from models.users_model import RoleTypes


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role: RoleTypes = RoleTypes.REGULAR_USER


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True


class LoginRequest(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    name: str


