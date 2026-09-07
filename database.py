import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Fallback to local SQLite if Postgres is not configured yet
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
if not SQLALCHEMY_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

# The connect_args={"check_same_thread": False} is only needed for SQLite in FastAPI
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        pool_pre_ping=True,       # Ping DB before using connection (drops dead ones)
        pool_recycle=300,         # Recycle connections every 5 minutes (prevents idle drops)
        pool_timeout=30,          # Don't hang forever waiting for pool
        connect_args={
            "connect_timeout": 15 # Give Neon up to 15 seconds to spin up compute
        }
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
