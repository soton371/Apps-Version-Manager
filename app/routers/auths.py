from typing import Optional
from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session
from app.schemas import auth_schema
from app.database import get_db
from app.custom_response import ResponseFailed, ResponseSuccess
from app.logging_config import logger
from app.services.auths_service import create_user
from app.models import auth_model
from app import utils


router = APIRouter(
    prefix="/auth",
    tags=['Auths']
)

# Use only for postman. Soton Ahmed will create user
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
    

@router.post('/login')
async def login(payload: auth_schema.UserCreate, db: Session = Depends(get_db)):
    try:
        exist_user = db.query(auth_model.User).filter(
            auth_model.User.email == payload.email).first()
        if not exist_user:
            return ResponseFailed(status_code=status.HTTP_404_NOT_FOUND, message=f'User with this {payload.email} email invalid')
        verify = utils.verify(payload.password, exist_user.password)
        if not verify:
            return ResponseFailed(
                status_code=status.HTTP_404_NOT_FOUND, message="Incorrect password")
        accessToken = oauth2.create_access_token(
            data={"user_id": exist_user.id})
        data = {"access_token": accessToken, "token_type": "Bearer"}
        return ResponseSuccess(status_code=status.HTTP_200_OK, data=data)
    except Exception as error:
        logger(f"login error: {error}")
        return ResponseFailed()
    
