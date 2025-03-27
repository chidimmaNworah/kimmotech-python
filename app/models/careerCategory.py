from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base, engine

class CareerCategory(Base):
    __tablename__ = "career_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    careers = relationship("Career", back_populates="category")

# CareerCategory.metadata.create_all(bind=engine)