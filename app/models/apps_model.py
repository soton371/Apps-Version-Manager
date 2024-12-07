from ..database import Base
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class Apps(Base):
    __tablename__ = "apps"

    id = Column(Integer, primary_key=True, nullable=False)
    package_name = Column(String, nullable=False, unique=True)
    play_store_version = Column(String, nullable=True)
    app_store_version = Column(String, nullable=True)
    force_update = Column(Boolean, nullable=True, server_default="FALSE")
    is_pause = Column(Boolean, nullable=True, server_default="FALSE")
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
