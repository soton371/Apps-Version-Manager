from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AppsCreate(BaseModel):
    app_name: Optional[str] = None
    package_name: str
    play_store_version: Optional[str] = None
    app_store_version: Optional[str] = None
    microsoft_store_version: Optional[str] = None
    force_update: Optional[bool] = False
    is_pause: Optional[bool] = False
    app_icon: Optional[str] = None
    play_store_link: Optional[str] = None
    app_store_link: Optional[str] = None
    microsoft_store_link: Optional[str] = None
    


class AppsOut(AppsCreate):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None

    class Config:
        from_attributes = True
