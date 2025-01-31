from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AuditTrailCreate(BaseModel):
    task_by: Optional[str] = None
    task: Optional[str] = None
    sector: Optional[str] = None
    impact: Optional[str] = None
    


class AuditTrailOut(AuditTrailCreate):
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


