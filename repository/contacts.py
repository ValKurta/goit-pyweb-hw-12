from sqlalchemy.orm import Session
from database.models import Contact


async def get_contacts(skip: int, limit: int, db: Session):
    return db.query(Contact).offset(skip).limit(limit).all()


def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()
