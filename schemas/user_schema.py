import re

from pydantic import BaseModel, EmailStr, Field, field_validator

from models.users_model import RoleTypes


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8, description="password should have at least 8 characters")
    role: RoleTypes = RoleTypes.REGULAR_USER

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str):

        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one number.")
        if not re.search(r"[@_!#$%^&*()<>?/\|}{~:]", v):
            raise ValueError("Password must contain at least one special character (@, _, etc.).")
        return v


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True


class LoginRequest(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    name: str
