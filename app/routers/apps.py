from fastapi import status, Depends, APIRouter
from app import schemas, models
from app.database import get_db
from sqlalchemy.orm import Session
from app.custom_response import ResponseFailed, ResponseSuccess
from icecream import ic


router = APIRouter(
    prefix="/apps",
    tags=['Apps']
)


@router.post('/')
async def create_apps(payload: schemas.AppsCreate, db: Session = Depends(get_db)):
    try:
        exist_app = db.query(models.Apps).filter(
            models.Apps.package_name == payload.package_name).first()

        if exist_app:
            return ResponseFailed(status_code=status.HTTP_208_ALREADY_REPORTED, message=f"App with package name {payload.package_name} already exists")

        new_app = models.Apps(**payload.model_dump())
        db.add(new_app)
        db.commit()
        db.refresh(new_app)

        return ResponseSuccess(message="A new app has been successfully added")
    except Exception as error:
        ic(error)
        return ResponseFailed(message=error)
