from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Set the DATABASE_URL (you can override this via environment variable)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://biomedlink_db_user:MOJnNWNkUckQ5XeyX63OESHRDVlIRJso@dpg-d1qm13c9c44c739ome00-a/biomedlink_db")

# Check if using SQLite or PostgreSQL
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
