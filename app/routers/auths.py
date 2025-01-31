from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from app.schemas import auth_schema
from app.core.database import get_db
from app.core.custom_response import ResponseFailed, ResponseSuccess
from app.core.utilities import logger
from app.core.oauth2 import getCurrentUser
from app.models import auth_model
from app.core import route_name
from app.services.auths_service import allUser, sendOtp, userCreate, userDelete, userLogin, userUpdate


router = APIRouter(
    prefix="",
    tags=['Auths']
)

    
@router.post(route_name.login)
async def login(payload: auth_schema.UserLogin, db: Session = Depends(get_db)):
    try:
        data = userLogin(payload=payload, db=db)
        return ResponseSuccess(status_code=status.HTTP_200_OK, data=data)

    except HTTPException as e:
        return ResponseFailed(status_code=e.status_code, message=e.detail)

    except Exception as error:
        logger(f"login error: {error}")
        return ResponseFailed()
    

@router.post(route_name.send_password)
async def sendPassword(payload: auth_schema.SendPassword, db: Session = Depends(get_db)):
    try:
        sendOtp(payload=payload, db=db)
        return ResponseSuccess(status_code=status.HTTP_200_OK, message="Password sent successfully")

    except HTTPException as e:
        return ResponseFailed(status_code=e.status_code, message=e.detail)
    
    except Exception as error:
        logger(f"sendPassword error: {error}")
        return ResponseFailed()


@router.post(route_name.user)
async def createUser(payload: auth_schema.UserCreate, db: Session = Depends(get_db), current_user: auth_model.User = Depends(getCurrentUser)):
    try:
        userCreate(payload=payload,db=db,current_user=current_user)
        return ResponseSuccess(status_code=status.HTTP_200_OK, message="User created successfully")
    
    except HTTPException as e:
        return ResponseFailed(status_code=e.status_code, message=e.detail)
    
    except Exception as error:
        logger(f"createUser error: {error}")
        return ResponseFailed(message="Failed to create user")
    

@router.get(route_name.user)
async def getAllUser(db: Session = Depends(get_db)):
    try:
        users = allUser(db=db)
        return ResponseSuccess(data=users)
    except Exception as error:
        logger(f"allUser error: {error}")
        return ResponseFailed()
    


@router.delete(f'{route_name.user}'+'/{user_id}')
async def deleteUser(user_id: int, db: Session = Depends(get_db), current_user: auth_model.User = Depends(getCurrentUser)):
    try:
        userDelete(user_id=user_id,db=db,current_user=current_user)
        return ResponseSuccess(status_code=status.HTTP_200_OK, message="User successfully deleted")
    
    except HTTPException as e:
        return ResponseFailed(status_code=e.status_code, message=e.detail)

    except Exception as error:
        logger(f"deleteUser error: {error}")
        return ResponseFailed(message="Failed to delete user")
    


@router.put(f'{route_name.user}'+'/{user_id}')
async def updateUser(user_id: int, payload: auth_schema.UserUpdate, db: Session = Depends(get_db), current_user: auth_model.User = Depends(getCurrentUser)):
    try:
        userUpdate(user_id=user_id,payload=payload,db=db,current_user=current_user)
        return ResponseSuccess(status_code=status.HTTP_200_OK, message="User updated successfully")
    
    except HTTPException as e:
        return ResponseFailed(status_code=e.status_code, message=e.detail)
    
    except Exception as error:
        logger(f"updateUser error: {error}")
        return ResponseFailed(message="Failed to update user")




