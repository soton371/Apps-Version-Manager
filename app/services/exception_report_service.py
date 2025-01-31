from typing import Optional
from fastapi import HTTPException,status
from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.models import apps_model, auth_model, exception_report_model
from app.schemas import audit_trail_schema, exception_report_schema
from app.core.utilities import booleanValue, my_timezone
from app.services.audit_trail_service import createAuditTrail
from datetime import datetime, timedelta
from app.core.database import get_db


def getExceptionReport(db: Session,
    limit: int = 20,
    skip: int = 0,
    search: Optional[str] = None,
    fixed: Optional[str] = None):
    # Base query
        query = db.query(exception_report_model.ExceptionReport)

        # Apply search filters
        if search:
            search = search.strip().lower()
            query = query.filter(
                exception_report_model.ExceptionReport.package_name.contains(search)
            )

        # Apply fixed filters
        if fixed:
            parse_fixed = booleanValue(fixed.lower())
            query = query.filter(
                exception_report_model.ExceptionReport.fixed == parse_fixed
            )

        # Order by created_at (latest to oldest) and paginate
        exception_reports = (
            query.order_by(desc(exception_report_model.ExceptionReport.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )


        # Serialize data
        exception_report_data = [
            exception_report_schema.ExceptionReportOut.model_validate(exception).model_dump()
            for exception in exception_reports
        ]

        return exception_report_data


def exceptionReportCreate(payload: exception_report_schema.ExceptionReportCreate, db: Session):
    exist_app = db.query(apps_model.Apps).filter(
    apps_model.Apps.package_name == payload.package_name).first()

    if not exist_app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{payload.package_name} not found')

    new_exception = exception_report_model.ExceptionReport(**payload.model_dump())
    db.add(new_exception)
    db.commit()


def exceptionReportUpdate(id: int, payload: exception_report_schema.ExceptionReportUpdate,db: Session, current_user: auth_model.User):
    exist_exception = db.query(exception_report_model.ExceptionReport).filter(
            exception_report_model.ExceptionReport.id == id).first()
    if not exist_exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Exception not found with {id}')
    exist_exception.fixed = payload.fixed
    audit_payload = audit_trail_schema.AuditTrailCreate(task_by=current_user.email, task= "Fixed", sector="Exception", impact=exist_exception.package_name)
    createAuditTrail(payload=audit_payload, db=db)
    
    if payload.fixed:
        one_month_ago = datetime.now(my_timezone) - timedelta(days=30)
        
        count = db.query(exception_report_model.ExceptionReport).filter(
        exception_report_model.ExceptionReport.created_at < one_month_ago
        ).count()

        if count > 0:
            db.query(exception_report_model.ExceptionReport).filter(
                exception_report_model.ExceptionReport.created_at < one_month_ago
            ).delete(synchronize_session=False)
    db.commit()

