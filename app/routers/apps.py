from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session
from app.schemas import apps_schema
from app.database import get_db
from app.services.apps_service import create_app, get_all_apps
from app.custom_response import ResponseFailed, ResponseSuccess
from app.logging_config import logger

router = APIRouter(
    prefix="/apps",
    tags=['Apps']
)

@router.post('/')
async def create_apps(payload: apps_schema.AppsCreate, db: Session = Depends(get_db)):
    try:
        app = create_app(payload, db)
        if not app:
            return ResponseFailed(status_code=status.HTTP_208_ALREADY_REPORTED,
                                message=f"App with package name {payload.package_name} already exists")
        return ResponseSuccess(message="A new app has been successfully added")
    except Exception as error:
        logger.debug(f"create_apps error: {error}")
        return ResponseFailed()

@router.get('/')
async def all_apps(db: Session = Depends(get_db)):
    try:
        apps = get_all_apps(db)
        if not apps:
            return ResponseFailed(status_code=status.HTTP_404_NOT_FOUND, message="No apps yet")
        apps_data = [apps_schema.AppsOut.model_validate(app).model_dump() for app in apps]
        logger.debug(f"apps_data: {apps_data}")
        return ResponseSuccess(data=apps_data)
    except Exception as error:
        logger.debug(f"all_apps error: {error}")
        return ResponseFailed()
