"""
Database Configuration and Setup
================================

SQLAlchemy configuration for the AI SQL generation system.
Supports both SQLite (development) and PostgreSQL (production).
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
from typing import Generator

# Database URL configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./ai_de_pair.db"  # Default to SQLite for development
)

# Create engine with appropriate configuration
if DATABASE_URL.startswith("sqlite"):
    # SQLite configuration for development
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=True  # Enable SQL logging in development
    )
else:
    # PostgreSQL configuration for production
    engine = create_engine(
        DATABASE_URL,
        echo=False  # Disable SQL logging in production
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base for models
Base = declarative_base()


def get_db() -> Generator:
    """
    Database dependency for FastAPI endpoints.
    
    Yields:
        Database session that will be automatically closed after use
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database by creating all tables.
    Call this when starting the application.
    """
    Base.metadata.create_all(bind=engine)


def drop_db():
    """
    Drop all database tables.
    Use with caution - only for testing/development reset.
    """
    Base.metadata.drop_all(bind=engine)
