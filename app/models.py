from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from .database import Base

class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    college_department = Column(String, nullable=True)
    registered_at = Column(DateTime, default=datetime.utcnow)
