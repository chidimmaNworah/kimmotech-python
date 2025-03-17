  
from sqlalchemy import Column, Integer, String, Text
from ..database import Base, engine

class About(Base):
    __tablename__ = "abouts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    img_url = Column(String(255), nullable=False)

About.metadata.create_all(bind=engine)