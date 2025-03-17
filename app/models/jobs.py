from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.dialects.postgresql import ARRAY  
from sqlalchemy.orm import relationship
from slugify import slugify
from ..database import Base, engine

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    excerpt = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    categories = Column(ARRAY(String), nullable=False)  # Array of category names
    industry = Column(String(255), nullable=True)
    field = Column(ARRAY(String), nullable=True)  # Array of job fields
    state = Column(String(255), nullable=True)
    region = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Define relationship with Comment
    comments = relationship("Comment", back_populates="job", cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.slug:
            self.slug = slugify(self.title)  # Auto-generate slug from title if empty
