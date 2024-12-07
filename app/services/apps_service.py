from sqlalchemy.orm import Session
from app import models, schemas

def create_app(payload: schemas.AppsCreate, db: Session):
    # Check if app exists
    exist_app = db.query(models.Apps).filter(
        models.Apps.package_name == payload.package_name).first()
    if exist_app:
        return None

    # Create new app
    new_app = models.Apps(**payload.model_dump())
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return new_app

def get_all_apps(db: Session):
    return db.query(models.Apps).all()
