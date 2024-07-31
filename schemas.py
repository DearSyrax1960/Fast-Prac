from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr


class UpdateUser(BaseModel):
    name: str


class Token(BaseModel):
    access_token: str
    token_type: str