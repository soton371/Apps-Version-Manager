from typing import Optional
from sqlalchemy.orm import Session
from app.schemas import apps_schema
from app.models import apps_model

def create_app(payload: apps_schema.AppsCreate, db: Session):
    # Check if app exists
    exist_app = db.query(apps_model.Apps).filter(
        apps_model.Apps.package_name == payload.package_name).first()
    if exist_app:
        return None

    # Create new app
    new_app = apps_model.Apps(**payload.model_dump())
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return new_app

def get_all_apps(db: Session, limit: int = None, skip: int = 0,
                    search: Optional[str] = ''):
    return db.query(apps_model.Apps).filter(apps_model.Apps.package_name.contains(search)).limit(limit).offset(skip).all()

def delete_app(id: int, db: Session):
    exist_app = db.query(apps_model.Apps).filter(
        apps_model.Apps.id == id)
    if not exist_app.first():
        return False
    exist_app.delete(synchronize_session=False)
    db.commit()
    return True