from typing import Optional
from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session
from app.schemas import auth_schema
from app.database import get_db
from app.custom_response import ResponseFailed, ResponseSuccess
from app.logging_config import logger
from app.services.auths_service import create_user


router = APIRouter(
    prefix="/auth",
    tags=['Auths']
)


@router.post('/create_user')
async def create_users(payload: auth_schema.UserCreate, db: Session = Depends(get_db)):
    try:
        user = create_user(payload=payload, db=db)
        if not user:
            return ResponseFailed(status_code=status.HTTP_208_ALREADY_REPORTED, message=f'User with email {payload.email} already exists')
        data = auth_schema.UserOut.model_validate(user).model_dump()
        return ResponseSuccess(message="User creation successful", data=data)
    except Exception as error:
        logger(f"create_users error: {error}")
        return ResponseFailed()
    
