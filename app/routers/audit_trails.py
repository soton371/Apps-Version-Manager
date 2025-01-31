from typing import Optional
from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.custom_response import ResponseFailed, ResponseSuccess
from app.services.audit_trail_service import getAuditTrails
from app.core.utilities import logger
from datetime import datetime
from app.core import route_name

router = APIRouter(
    prefix="",
    tags=['Audit Trails']
)


@router.get(route_name.audit_trail)
async def allAuditTrails(
    db: Session = Depends(get_db),
    limit: int = 20,
    skip: int = 0,
    search: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
    ):
    
    try:
        audit_trail_data = getAuditTrails(db=db,limit=limit, skip=skip, search=search, start_date=start_date, end_date=end_date)
        return ResponseSuccess(data=audit_trail_data)

    except Exception as error:
        logger(f"Error in get_audit_trails: {error}")
        return ResponseFailed(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message= "Failed to get all audit trails"
        )
    


