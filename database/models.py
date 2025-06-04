from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    pass


class DBCookie(Base):
    __tablename__ = "cookie"
    name = Column(String, primary_key=True)
    value = Column(String, primary_key=True)
    expires = Column(DateTime, primary_key=True)

    def __repr__(self):
        return f"Cookie(name={self.name}, value={self.value}, expires={self.expires})"
