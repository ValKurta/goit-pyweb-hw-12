from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import ContactBase, ContactCreate, ContactUpdate, ContactInDB
from repository.contacts import (get_contacts, get_contact, create_contact as create_contact_in_db,
                                 update_contact as update_contact_in_db, delete_contact as delete_contact_in_db,
                                 search_contacts as search_contacts_in_db, get_upcoming_birthdays)
from services.auth import auth_service
from database.db import get_db
from database.models import User
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

router = APIRouter(prefix="/contacts", tags=["contacts"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    if not token:  # Проверяем, если токен пустой
        return None  # Возвращаем None, если токена нет
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None  # Если email отсутствует
    except JWTError:
        return None  # Если произошла ошибка декодирования

    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        return None  # Если пользователь не найден
    return user



@router.post("/", response_model=ContactInDB)
async def create_contact_endpoint(contact: ContactCreate, db: Session = Depends(get_db),
                                  current_user: User = Depends(get_current_user)):
    return create_contact_in_db(db=db, contact=contact)


@router.get("/contacts", response_model=list[ContactInDB])
async def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    contacts = get_contacts(db, skip=skip, limit=limit)
    return contacts



@router.get("/{contact_id}", response_model=ContactInDB)
async def read_contact(contact_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    contact = get_contact(db, contact_id=contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.put("/{contact_id}", response_model=ContactInDB)
async def update_contact_endpoint(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db),
                                  current_user: User = Depends(get_current_user)):
    db_contact = update_contact_in_db(db=db, contact_id=contact_id, contact=contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.delete("/{contact_id}", response_model=ContactInDB)
async def delete_contact_endpoint(contact_id: int, db: Session = Depends(get_db),
                                  current_user: User = Depends(get_current_user)):
    db_contact = delete_contact_in_db(db=db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.get("/search/", response_model=list[ContactInDB])
async def search_contacts_endpoint(query: str, db: Session = Depends(get_db),
                                   current_user: User = Depends(get_current_user)):
    contacts = search_contacts_in_db(db=db, query=query)
    return contacts

@router.get("/upcoming-birthdays/", response_model=list[ContactInDB])
async def upcoming_birthdays(db: Session = Depends(get_db),
                             current_user: User = Depends(get_current_user)):
    try:
        contacts = get_upcoming_birthdays(db=db)
        return contacts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
