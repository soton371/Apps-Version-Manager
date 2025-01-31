from typing import Optional
from fastapi import HTTPException, Depends, APIRouter, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.schemas import apps_schema
from app.models import auth_model
from app.core.database import get_db
from app.services.apps_service import createApp, getAllApps, deleteApp, updateApp, singleApp
from app.core.custom_response import ResponseFailed, ResponseSuccess
from app.core.oauth2 import getCurrentUser
from app.core.utilities import booleanValue, logger
from app.core import route_name

router = APIRouter(
    prefix="",
    tags=['Apps']
)



@router.post(route_name.apps)
async def createApps(
    app_name: str = Form(None),
    package_name: str = Form(...),
    play_store_version: Optional[str] = Form(None),
    app_store_version: Optional[str] = Form(None),
    microsoft_store_version: Optional[str] = Form(None),
    force_update: Optional[str] = Form(None),
    is_pause: Optional[str] = Form(None),
    play_store_link: Optional[str] = Form(None),
    app_store_link: Optional[str] = Form(None),
    microsoft_store_link: Optional[str] = Form(None),
    app_icon: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: auth_model.User = Depends(getCurrentUser)
):
    try:       
        # Prepare payload
        payload = apps_schema.AppsCreate(
            app_name=app_name,
            package_name=package_name,
            play_store_version=play_store_version,
            app_store_version=app_store_version,
            microsoft_store_version=microsoft_store_version,
            force_update=booleanValue(force_update),
            is_pause=booleanValue(is_pause),
            play_store_link=play_store_link,
            app_store_link=app_store_link,
            microsoft_store_link=microsoft_store_link,
            app_icon=None
        )


        createApp(payload=payload, db=db, current_user= current_user, app_icon=app_icon)
        return ResponseSuccess(message="A new app has been successfully added")
    except HTTPException as e:
        return ResponseFailed(message=e.detail, status_code=e.status_code)
    except Exception as error:
        logger(f"createApps error: {error} line: {error.__traceback__.tb_lineno}")
        return ResponseFailed(message='Failed to create app')



@router.get(route_name.apps)
async def allApps(db: Session = Depends(get_db)):
    try:
        apps = getAllApps(db)
        return ResponseSuccess(data=apps)
    except Exception as error:
        logger(f"allApps error: {error}")
        return ResponseFailed(message="Failed to get all app")


@router.delete(f"{route_name.apps}"+'/{id}')
async def deleteApps(id: int, db: Session = Depends(get_db), current_user: auth_model.User = Depends(getCurrentUser)):
    try:
        deleteApp(id=id, db=db, current_user=current_user)
        return ResponseSuccess(message="The app was successfully deleted")
    except HTTPException as e:
        return ResponseFailed(message=e.detail, status_code=e.status_code)
    except Exception as error:
        logger(f"deleteApps error: {error} {error.__traceback__}")
        return ResponseFailed(message="Failed to delete app")


@router.put(f"{route_name.apps}"+'/{id}')
async def updateApps(
    id: int, 
    app_name: str = Form(None),
    package_name: str = Form(...),
    play_store_version: Optional[str] = Form(None),
    app_store_version: Optional[str] = Form(None),
    microsoft_store_version: Optional[str] = Form(None),
    force_update: Optional[str] = Form(None),
    is_pause: Optional[str] = Form(None),
    play_store_link: Optional[str] = Form(None),
    app_store_link: Optional[str] = Form(None),
    microsoft_store_link: Optional[str] = Form(None),
    app_icon: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: auth_model.User = Depends(getCurrentUser)):
# async def updateApps(id: int, payload: apps_schema.AppsCreate, db: Session = Depends(get_db), current_user: auth_model.User = Depends(getCurrentUser), app_icon: Optional[UploadFile] = File(None),):
    try:
        payload = apps_schema.AppsCreate(
            app_name=app_name,
            package_name=package_name,
            play_store_version=play_store_version,
            app_store_version=app_store_version,
            microsoft_store_version=microsoft_store_version,
            force_update=booleanValue(force_update),
            is_pause=booleanValue(is_pause),
            play_store_link=play_store_link,
            app_store_link=app_store_link,
            microsoft_store_link=microsoft_store_link,
            app_icon=None
        )
        updateApp(id=id, payload=payload, db=db, current_user=current_user, app_icon=app_icon)
        return ResponseSuccess(message="The app has been successfully updated")
    except HTTPException as e:
        return ResponseFailed(message=e.detail, status_code=e.status_code)
    except Exception as error:
        logger(f"updateApps error: {error}")
        return ResponseFailed(message="Failed to update app")
    

@router.get(f'{route_name.apps}'+'/{package_name}')
async def singleApps(package_name: str, db: Session = Depends(get_db)):
    try:
        app = singleApp(package_name=package_name, db=db)
        return ResponseSuccess(data=app)
    except HTTPException as e:
        return ResponseFailed(message=e.detail, status_code=e.status_code)
    except Exception as error:
        logger(f"singleApps error: {error}")
        return ResponseFailed(message="Failed to get app")
    
    