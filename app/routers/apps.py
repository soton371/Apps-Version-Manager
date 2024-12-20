from typing import Optional
from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session
from app.schemas import apps_schema
from app.database import get_db
from app.services.apps_service import create_app, get_all_apps, delete_app, update_app, single_app
from app.custom_response import ResponseFailed, ResponseSuccess
from app.logging_config import logger
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/apps",
    tags=['Apps']
)


@router.post('/')
async def create_apps(payload: apps_schema.AppsCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    try:
        app = create_app(payload, db)
        if not app:
            return ResponseFailed(status_code=status.HTTP_208_ALREADY_REPORTED,
                                  message=f"App with package name {payload.package_name} already exists")
        return ResponseSuccess(message="A new app has been successfully added")
    except Exception as error:
        logger(f"create_apps error: {error}")
        return ResponseFailed()


@router.get('/')
async def all_apps(db: Session = Depends(get_db), limit: int = None, skip: int = 0,
                   search: Optional[str] = ''):
    try:
        apps = get_all_apps(db=db, limit=limit, skip=skip, search=search)
        if not apps:
            return ResponseFailed(status_code=status.HTTP_404_NOT_FOUND, message="No apps yet")
        apps_data = [apps_schema.AppsOut.model_validate(
            app).model_dump() for app in apps]
        return ResponseSuccess(data=apps_data)
    except Exception as error:
        logger(f"all_apps error: {error}")
        return ResponseFailed()


@router.delete("/{id}")
async def delete_apps(id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    try:
        is_delete_app = delete_app(id=id, db=db)
        if is_delete_app:
            return ResponseSuccess(message="The app was successfully deleted")
        else:
            return ResponseFailed(message=f"No app found with id {id}", status_code=status.HTTP_404_NOT_FOUND)
    except Exception as error:
        logger(f"delete_apps error: {error}")
        return ResponseFailed()


@router.put('/{id}')
async def update_apps(id: int, payload: apps_schema.AppsCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    try:
        is_update_app = update_app(id=id, payload=payload, db=db)
        if is_update_app:
            return ResponseSuccess(message="The app has been successfully updated")
        else:
            return ResponseFailed(status_code=status.HTTP_404_NOT_FOUND, message=f"No app found with id {id}")
    except Exception as error:
        logger(f"update_apps error: {error}")
        return ResponseFailed()
    

@router.get('/{package_name}')
async def single_apps(package_name: str, db: Session = Depends(get_db)):
    try:
        app = single_app(package_name=package_name, db=db)
        if not app:
            return ResponseFailed(status_code=status.HTTP_404_NOT_FOUND,message=f"No app found with {package_name}")
        data = apps_schema.AppsOut.model_validate(app).model_dump()
        return ResponseSuccess(data=data)
    except Exception as error:
        logger(f"single_apps error: {error}")
        return ResponseFailed()