from pydantic import BaseModel

from datetime import datetime

class BaseCookie(BaseModel):
    name: str

class ValuedCookie(BaseCookie):
    value: str

class TimedCookie(BaseCookie):
    expires: datetime

class FullCookie(ValuedCookie):
    expires: datetime

class ResponseCookie(BaseModel):
    message: str
    data: ValuedCookie
