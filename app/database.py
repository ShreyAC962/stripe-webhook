from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL) 

# Create a new session for each request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

# Base class for our models
Base = declarative_base()