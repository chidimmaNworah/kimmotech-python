from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, func
from sqlalchemy.dialects.postgresql import ARRAY  
from sqlalchemy.orm import relationship
from slugify import slugify
from ..database import Base, engine

class Career(Base):
    __tablename__ = "careers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    excerpt = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    industry = Column(String(255), nullable=True)
    field = Column(ARRAY(String), nullable=True)
    state = Column(String(255), nullable=True)
    region = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    category_id = Column(Integer, ForeignKey("career_categories.id"), nullable=False)
    category = relationship("CareerCategory", back_populates="careers")

    comments = relationship("Comment", back_populates="career", cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.slug:
            self.slug = slugify(self.title)

# Career.metadata.create_all(bind=engine)