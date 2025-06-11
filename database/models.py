from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    pass


class DBCookie(Base):
    """
    Represents a cookie stored in the database.
        ``name`` (str): The name of the cookie.
        ``value`` (str): The name of the cookie.
        ``expires`` (datetime): The name of the cookie.
    """
    __tablename__ = "cookie"
    name = Column(String, primary_key=True)
    value = Column(String, primary_key=True)
    expires = Column(DateTime, primary_key=True)

    def __repr__(self):
        return f"Cookie(name={self.name}, value={self.value}, expires={self.expires})"

class Authentication(Base):
    __tablename__ = "authentication"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    mail = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    password = Column(String, nullable=False)

    def __repr__(self):
        return f"Authentication(id={self.id}, name={self.name}, mail={self.mail}, password={self.password})"
