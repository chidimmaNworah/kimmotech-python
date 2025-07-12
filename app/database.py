# app/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# DB_NAME = os.getenv("DB_NAME")
# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_HOST = os.getenv("DB_HOST")
# DB_PORT = os.getenv("DB_PORT")

DATABASE_URL = os.getenv("DB_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in environment variables!")

engine = None
SessionLocal = None

Base = declarative_base()

def get_engine():
    global engine
    if engine is None:
        engine = create_engine(
            DATABASE_URL,
            pool_size=5,
            max_overflow=2,
            pool_timeout=30,
            pool_pre_ping=True
        )
    return engine

def get_session_local():
    global SessionLocal
    if SessionLocal is None:
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=get_engine()
        )
    return SessionLocal

def get_db():
    session = get_session_local()()
    try:
        yield session
    finally:
        session.close()
