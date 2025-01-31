from typing import Optional
from pydantic import BaseModel
from datetime import datetime



class ExceptionReportCreate(BaseModel):
    package_name: Optional[str] = None
    url: Optional[str] = None
    payload: Optional[str] = None
    exception: Optional[str] = None
    exception_line: Optional[str] = None
    fixed: Optional[bool] = False
    



class ExceptionReportOut(ExceptionReportCreate):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    # fixed: bool

    class Config:
        from_attributes = True



class ExceptionReportUpdate(BaseModel):
    fixed: bool
    

    