from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import Date, cast, desc, or_
from sqlalchemy.orm import Session
from app.schemas import audit_trail_schema
from app.models import  audit_trail_model
from app.core.utilities import logger, my_timezone


def createAuditTrail(payload: audit_trail_schema.AuditTrailCreate, db: Session):
    try:
        new_app = audit_trail_model.AuditTrail(**payload.model_dump())
        db.add(new_app)
        one_month_ago = datetime.now(my_timezone) - timedelta(days=30)
        
        count = db.query(audit_trail_model.AuditTrail).filter(
        audit_trail_model.AuditTrail.created_at < one_month_ago
        ).count()

        if count > 0:
            db.query(audit_trail_model.AuditTrail).filter(
                audit_trail_model.AuditTrail.created_at < one_month_ago
            ).delete(synchronize_session=False)
    except Exception as error:
        logger(f"Error in create_audit_trail: {error}")





def getAuditTrails(db: Session,
    limit: int,
    skip: int,
    search: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None):
    # Base query
    query = db.query(audit_trail_model.AuditTrail)

    # Apply search filters
    if search:
        search = search.strip()
        query = query.filter(
            or_(
                audit_trail_model.AuditTrail.task.contains(search),
                audit_trail_model.AuditTrail.sector.contains(search),
                audit_trail_model.AuditTrail.impact.contains(search),
                audit_trail_model.AuditTrail.task_by.contains(search)
            )
        )

    # Apply date range filters
    if start_date and end_date:
        query = query.filter(
            cast(audit_trail_model.AuditTrail.created_at, Date).between(
                start_date.date(), end_date.date()
            )
        )

    # Order by created_at (latest to oldest) and paginate
    audit_trails = (
        query.order_by(desc(audit_trail_model.AuditTrail.created_at))
        .offset(skip)
        .limit(limit)
        .all()
    )

    audit_trail_data = [
        audit_trail_schema.AuditTrailOut.model_validate(trail).model_dump()
        for trail in audit_trails
    ]

    return audit_trail_data

