from pydantic import BaseModel,EmailStr
from datetime import datetime


class BookingCreate(BaseModel):
    full_name:str
    email:EmailStr
    timestamp: datetime

