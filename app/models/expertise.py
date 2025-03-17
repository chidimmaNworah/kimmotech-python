from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSON
from ..database import Base, engine

class Expertise(Base):
    __tablename__ = "expertise"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    img_url = Column(JSON, default=[])

Expertise.metadata.create_all(bind=engine)