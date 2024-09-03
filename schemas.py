from pydantic import BaseModel
from datetime import date
from typing import Optional


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    birthday: date
    additional_info: Optional[str] = None


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None  # Поле phone
    birthday: Optional[date] = None  # Поле birthday
    additional_info: Optional[str] = None


class ContactInDB(ContactBase):
    id: int

    class Config:
        from_attributes = True
