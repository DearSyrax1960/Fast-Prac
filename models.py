from sqlalchemy import Column, Integer, String, Enum as SQLAEnum
from sqlalchemy.orm import declarative_base

from enum import Enum

Base = declarative_base()


class RoleTypes(str, Enum):
    ADMIN = 'ADMIN',
    REGULAR_USER = 'REGULAR_USER'


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(SQLAEnum(RoleTypes), default=RoleTypes.REGULAR_USER)
