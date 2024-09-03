from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.db import get_db
from schemas import ContactBase, ContactCreate, ContactUpdate, ContactInDB
from repository.contacts import (get_contacts, get_contact, create_contact as create_contact_in_db,
                                 update_contact as update_contact_in_db, delete_contact as delete_contact_in_db,
                                 search_contacts as search_contacts_in_db, get_upcoming_birthdays)

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/contacts", response_model=ContactInDB)
def create_contact_endpoint(contact: ContactCreate, db: Session = Depends(get_db)):
    return create_contact_in_db(db=db, contact=contact)


@router.get("/contacts", response_model=list[ContactInDB])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    contacts = get_contacts(db, skip=skip, limit=limit)
    return contacts


@router.get("/contacts/{contact_id}", response_model=ContactInDB)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = get_contact(db, contact_id=contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/contacts/{contact_id}", response_model=ContactInDB)
def update_contact_endpoint(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    db_contact = update_contact_in_db(db=db, contact_id=contact_id, contact=contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.delete("/contacts/{contact_id}", response_model=ContactInDB)
def delete_contact_endpoint(contact_id: int, db: Session = Depends(get_db)):
    db_contact = delete_contact_in_db(db=db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.get("/contacts/search/", response_model=list[ContactInDB])
def search_contacts_endpoint(query: str, db: Session = Depends(get_db)):
    contacts = search_contacts_in_db(db=db, query=query)
    return contacts


@router.get("/contacts/upcoming-birthdays/", response_model=list[ContactInDB])
def upcoming_birthdays(db: Session = Depends(get_db)):
    try:
        contacts = get_upcoming_birthdays(db=db)
        return contacts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

