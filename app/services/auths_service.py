from typing import Optional
from sqlalchemy.orm import Session
from app import utils
from app.schemas import auth_schema
from app.models import auth_model


def create_user(payload: auth_schema.UserCreate, db: Session):
    exist_user = db.query(auth_model.User).filter(
            auth_model.User.email == payload.email).first()
    if exist_user:
        return None
    hashedPassword = utils.hashedPassword(payload.password)
    payload.password = hashedPassword
    new_user = auth_model.User(**payload.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user