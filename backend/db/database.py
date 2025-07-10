from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./biomedlink.db"  # For Render, we will update this to PostgreSQL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# ✅ Add this to fix the import error
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
