from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Date, Float
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
    __tablename__ = "service_orders"

    id = Column(Integer, primary_key=True, index=True)
    engineer_name = Column(String, nullable=False)
    issue = Column(String, nullable=False)
    spare_parts = Column(String, nullable=True)
    arrival_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=False)
    mission_fee = Column(Float, nullable=False)
    transport_fee = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=False)
    user_id = Column(Integer, nullable=False)
