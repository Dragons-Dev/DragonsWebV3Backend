from pydantic import BaseModel

from datetime import datetime


class Cookie(BaseModel):
    name: str
    value: str
    expires: datetime
