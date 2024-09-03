from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.db import get_db
from schemas import Contact, ContactCreate, ContactUpdate
from repository.contacts import get_contacts, get_contact

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[Contact])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = await get_contacts(skip, limit, db)
    return contacts


@router.get("/contacts/{contact_id}", response_model=Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact
