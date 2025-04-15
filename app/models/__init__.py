from .careerCategory import CareerCategory
from .category import Category
from .careers import Career
from .user import Comment, User, Message
from .project import Project
from .about import About
from .expertise import Expertise
from .newsletter import Newsletter
from ..database import Base, engine

print("Creating tables in order...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")