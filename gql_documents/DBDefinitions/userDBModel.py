import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
)
from .UUID import UUIDColumn, UUIDFKey
from .Base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    id = UUIDColumn()

    name = Column(String)
    surname = Column(String)
    email = Column(String, nullable=True)

    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
