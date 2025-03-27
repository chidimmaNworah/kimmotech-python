from sqlalchemy import Column, Integer, String, DateTime, func
from ..database import Base, engine

class Newsletter(Base):
    __tablename__ = "newsletters"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    platform = Column(String(100), unique=False, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

# Newsletter.metadata.create_all(bind=engine)