from ..core.database import Base
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class ExceptionReport(Base):
    __tablename__ = "exception_report"

    id = Column(Integer, primary_key=True, nullable=False)
    package_name = Column(String, nullable=True)
    url = Column(String, nullable=True)
    payload = Column(String, nullable=True)
    exception = Column(String, nullable=True)
    exception_line = Column(String, nullable=True)
    fixed = Column(Boolean, nullable=False, server_default=text("false"))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))


