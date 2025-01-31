from typing import Optional
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app.core.oauth2 import getCurrentUser
from app.schemas import exception_report_schema, audit_trail_schema
from app.models import exception_report_model, apps_model, auth_model
from app.core.database import get_db
from app.core.custom_response import ResponseFailed, ResponseSuccess
from app.services.audit_trail_service import createAuditTrail
from app.services.exception_report_service import exceptionReportCreate, exceptionReportUpdate, getExceptionReport
from app.core.utilities import logger
from app.core import route_name

router = APIRouter(
    prefix="",
    tags=['Exception Report']
)


@router.post(route_name.exception_report)
async def createExceptionReport(payload: exception_report_schema.ExceptionReportCreate, db: Session = Depends(get_db)):
    try:
        exceptionReportCreate(payload=payload, db=db)
        return ResponseSuccess(message="Exception report created")
    
    except HTTPException as e:
        return ResponseFailed(status_code=e.status_code, message=e.detail)
    
    except Exception as error:
        logger(f"createExceptionReport error: {error}")
        return ResponseFailed(message="An error occurred while create exception report")




@router.get(route_name.exception_report)
async def allExceptionReport(
    db: Session = Depends(get_db),
    limit: int = 20,
    skip: int = 0,
    search: Optional[str] = None,
    fixed: Optional[str] = None
):

    try:
        exception_report_data = getExceptionReport(db=db,limit=limit,skip=skip,search=search,fixed=fixed)
        return ResponseSuccess(data=exception_report_data)

    except Exception as error:
        logger(f"Error in getExceptionReport: {error}")
        return ResponseFailed(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="An error occurred while fetching exception report"
        )



@router.put(f'{route_name.exception_report}'+'/{id}')
async def updateExceptionReport(id: int, payload: exception_report_schema.ExceptionReportUpdate,db: Session = Depends(get_db), current_user: auth_model.User = Depends(getCurrentUser)):
    try:
        exceptionReportUpdate(id=id,payload=payload,db=db,current_user=current_user)
        return ResponseSuccess(message="Exception report updated successfully")
    
    except HTTPException as e:
        return ResponseFailed(status_code=e.status_code, message=e.detail)
    
    except Exception as error:
        logger(f"Error in updateExceptionReport: {error}")
        return ResponseFailed(message="An error occurred while update exception report")
    

