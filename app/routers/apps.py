from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session
from app import schemas
from app.database import get_db
from app.services.apps_service import create_app, get_all_apps
from app.custom_response import ResponseFailed, ResponseSuccess

router = APIRouter(
    prefix="/apps",
    tags=['Apps']
)

@router.post('/')
async def create_apps(payload: schemas.AppsCreate, db: Session = Depends(get_db)):
    app = create_app(payload, db)
    if not app:
        return ResponseFailed(status_code=status.HTTP_208_ALREADY_REPORTED,
                              message=f"App with package name {payload.package_name} already exists")
    return ResponseSuccess(message="A new app has been successfully added")

@router.get('/')
async def all_apps(db: Session = Depends(get_db)):
    apps = get_all_apps(db)
    if not apps:
        return ResponseFailed(status_code=status.HTTP_404_NOT_FOUND, message="No apps yet")
    return ResponseSuccess(data=[schemas.AppsOut.model_validate(app) for app in apps])
