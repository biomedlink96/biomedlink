from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from .database import Base
from sqlalchemy.orm import relationship

# ---------------- User Model ----------------
class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}  # 👈 Optional safety for hot reloads

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    jobcards = relationship("JobCard", back_populates="user", cascade="all, delete-orphan")
    serviceorders = relationship("ServiceOrder", back_populates="user", cascade="all, delete-orphan")

# ---------------- JobCard Model ----------------
class JobCard(Base):
    __tablename__ = "jobcards"

    id = Column(Integer, primary_key=True, index=True)
    equipment_name = Column(String)
    maintenance_type = Column(String)
    date_of_service = Column(DateTime, default=datetime.utcnow)
    spare_parts_used = Column(Text)
    file_path = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="jobcards")

# ---------------- ServiceOrder Model ----------------
class ServiceOrder(Base):
    __tablename__ = "serviceorders"

    id = Column(Integer, primary_key=True, index=True)
    issue = Column(Text)
    spare_parts = Column(Text)
    date = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="serviceorders")
