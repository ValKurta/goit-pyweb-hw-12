from datetime import date, timedelta

from fastapi import HTTPException
from sqlalchemy import extract, or_, and_

from sqlalchemy.orm import Session
from database.models import Contact
from schemas import ContactBase, ContactCreate, ContactUpdate, ContactInDB
import logging

logger = logging.getLogger("uvicorn.error")


def create_contact(db: Session, contact: ContactCreate):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def get_contacts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Contact).offset(skip).limit(limit).all()


def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()


def update_contact(db: Session, contact_id: int, contact: ContactUpdate):
    db_contact = get_contact(db, contact_id)
    if db_contact is None:
        return None
    for key, value in contact.dict(exclude_unset=True).items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int):
    db_contact = get_contact(db, contact_id)
    if db_contact is None:
        return None
    db.delete(db_contact)
    db.commit()
    return db_contact


def search_contacts(db: Session, query: str):
    return db.query(Contact).filter(
        Contact.first_name.contains(query) |
        Contact.last_name.contains(query) |
        Contact.email.contains(query)
    ).all()


def get_upcoming_birthdays(db: Session):
    try:
        logger.debug("Starting get_upcoming_birthdays function")
        today = date.today()
        logger.debug(f"Today's date: {today}")
        upcoming = today + timedelta(days=7)
        logger.debug(f"Upcoming date: {upcoming}")

        if today.month == 12 and upcoming.month == 1:
            logger.debug("End of year logic triggered")
            contacts = db.query(Contact).filter(
                or_(
                    and_(
                        extract('month', Contact.birthday) == today.month,
                        extract('day', Contact.birthday) >= today.day
                    ),
                    and_(
                        extract('month', Contact.birthday) == upcoming.month,
                        extract('day', Contact.birthday) <= upcoming.day
                    )
                )
            ).all()
        else:
            logger.debug("Regular logic triggered")
            contacts = db.query(Contact).filter(
                or_(
                    and_(
                        extract('month', Contact.birthday) == today.month,
                        extract('day', Contact.birthday) >= today.day
                    ),
                    and_(
                        extract('month', Contact.birthday) == upcoming.month,
                        extract('day', Contact.birthday) <= upcoming.day
                    )
                )
            ).all()

        logger.debug(f"Number of contacts found: {len(contacts)}")
        return contacts
    except Exception as e:
        logger.error(f"An error occurred: {e}")
