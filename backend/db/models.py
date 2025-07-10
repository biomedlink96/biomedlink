from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class JobCard(Base):
    __tablename__ = "jobcards"

    id = Column(Integer, primary_key=True, index=True)
    equipment_name = Column(String)
    maintenance_type = Column(String)
    date_of_service = Column(DateTime, default=datetime.utcnow)
    spare_parts_used = Column(String)
    file_path = Column(String)


class JobCard(Base):
    __tablename__ = "jobcards"
    id = Column(Integer, primary_key=True, index=True)
    equipment = Column(String)
    maintenance_type = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)

class ServiceOrder(Base):
    __tablename__ = "serviceorders"
    id = Column(Integer, primary_key=True, index=True)
    issue = Column(Text)
    spare_parts = Column(Text)
    date = Column(DateTime, default=datetime.utcnow)
