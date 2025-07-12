from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship
from ..database import Base, engine

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=True )

    # @classmethod
    # def hash_password(cls, password: str) -> str:
    #     """Hashes a password using bcrypt."""
    #     return pwd_context.hash(password)

# User.metadata.create_all(bind=engine)

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

# Message.metadata.create_all(bind=engine)

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    career_id = Column(Integer, ForeignKey("careers.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)  # Name of the commenter
    email = Column(String(255), nullable=False)  # Email of the commenter
    content = Column(Text, nullable=False)  # Comment content
    created_at = Column(DateTime, server_default=func.now())

    # Define relationship with Job
    career = relationship("Career", back_populates="comments")

# Comment.metadata.create_all(bind=engine)