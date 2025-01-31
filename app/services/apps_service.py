from sqlalchemy.orm import Session
from app.schemas import apps_schema, audit_trail_schema
from app.models import apps_model, auth_model
from app.services.audit_trail_service import createAuditTrail
from sqlalchemy import desc
from fastapi import HTTPException, UploadFile, status
from app.core.utilities import uploadToS3
from typing import Optional


#check file type
allowed_image_types = [
        "image/jpeg",  # JPEG
        "image/png",   # PNG
        "image/gif",   # GIF
        "image/webp",  # WEBP
        "image/bmp",   # BMP
        "image/tiff",  # TIFF
        "image/x-icon" # ICO
    ]


def createApp(payload: apps_schema.AppsCreate, db: Session, current_user: auth_model.User, app_icon: UploadFile):
    # Check if app exists
    exist_app = db.query(apps_model.Apps).filter(
        apps_model.Apps.package_name == payload.package_name).first()
    if exist_app:
        raise HTTPException(
            status_code=status.HTTP_208_ALREADY_REPORTED,
            detail=f"App with package name {payload.package_name} already exists"
        )

        
    if app_icon.content_type not in allowed_image_types:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid file type. Only image files are allowed (JPEG, PNG, GIF, WEBP, BMP, TIFF, ICO)"
        )
    

    # upload the image
    app_icon_url = uploadToS3(app_icon, "app_icons")

    if app_icon_url is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to upload file"
        )

    
    payload.app_icon = app_icon_url
    
    # Create new app
    new_app = apps_model.Apps(**payload.model_dump())
    new_app.created_by = current_user.email
    db.add(new_app)
    audit_payload = audit_trail_schema.AuditTrailCreate(task_by=current_user.email, task= "Create",sector="App", impact=payload.package_name)
    createAuditTrail(payload=audit_payload, db=db)
    db.commit()
    db.refresh(new_app)
    

def getAllApps(db: Session):
    query = db.query(apps_model.Apps).order_by(desc(apps_model.Apps.created_at))
    apps_data = [
        apps_schema.AppsOut.model_validate(app).model_dump()
        for app in query.all()
    ]
    return apps_data



def deleteApp(id: int, db: Session, current_user: auth_model.User):
    exist_app = db.query(apps_model.Apps).filter(
        apps_model.Apps.id == id)
    
    if not exist_app.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No app found with id {id}"
        )
    package_name = exist_app.first().package_name
    exist_app.delete(synchronize_session=False)
    audit_payload = audit_trail_schema.AuditTrailCreate(task_by=current_user.email, task= "Delete",sector="App", impact=package_name)
    createAuditTrail(payload=audit_payload, db=db)
    db.commit()


def updateApp(id: int, payload: apps_schema.AppsCreate, db: Session, current_user: auth_model.User, app_icon: Optional[UploadFile]=None):
    exist_app = db.query(apps_model.Apps).filter(
        apps_model.Apps.id == id)
    if not exist_app.first():
        raise HTTPException(
            status_code=status.HTTP_208_ALREADY_REPORTED,
            detail=f"App with id {id} not exists"
        )
    
    app_icon_url = None

    if app_icon is not None:
        if app_icon.content_type not in allowed_image_types:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Invalid file type. Only image files are allowed (JPEG, PNG, GIF, WEBP, BMP, TIFF, ICO)"
            )
        app_icon_url = uploadToS3(app_icon, "app_icons")
    else:
        app_icon_url = exist_app.first().app_icon
    
    exist_app.update(payload.model_dump(), synchronize_session=False)
    exist_app.first().updated_by = current_user.email
    exist_app.first().app_icon = app_icon_url
    audit_payload = audit_trail_schema.AuditTrailCreate(task_by=current_user.email, task= "Update",sector="App", impact=exist_app.first().package_name)
    createAuditTrail(payload=audit_payload, db=db)
    db.commit()


def singleApp(package_name: str, db: Session):
    exist_app = db.query(apps_model.Apps).filter(
        apps_model.Apps.package_name == package_name.strip()).first()
    
    if not exist_app:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No app found with package name {package_name}"
        )
    
    app_dump = apps_schema.AppsOut.model_validate(exist_app).model_dump()
    
    return app_dump

