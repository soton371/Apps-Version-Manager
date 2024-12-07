from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AppsCreate(BaseModel):
    package_name: str
    play_store_version: Optional[str] = None
    app_store_version: Optional[str] = None
    force_update: Optional[bool] = False
    is_pause: Optional[bool] = False


class AppsOut(AppsCreate):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
