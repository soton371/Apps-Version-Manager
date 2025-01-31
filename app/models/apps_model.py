from app.core.database import Base
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.sql import func


class Apps(Base):
    __tablename__ = "apps"

    id = Column(Integer, primary_key=True, nullable=False)
    app_name = Column(String, nullable=True)
    package_name = Column(String, nullable=False, unique=True)
    play_store_version = Column(String, nullable=True)
    app_store_version = Column(String, nullable=True)
    microsoft_store_version = Column(String, nullable=True)
    force_update = Column(Boolean, nullable=True, server_default="FALSE")
    is_pause = Column(Boolean, nullable=True, server_default="FALSE")
    app_icon = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), onupdate=func.now())
    created_by = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)
    play_store_link = Column(String, nullable=True)
    app_store_link = Column(String, nullable=True)
    microsoft_store_link = Column(String, nullable=True)

