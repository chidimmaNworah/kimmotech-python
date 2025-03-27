from sqlalchemy.orm import Session
from .models import About, Category, User, Project, Expertise
from .schemas import AboutCreate, CategoryCreate, ProjectCreate, ProjectResponse, ExpertiseBase
import os
from dotenv import load_dotenv
from .utils.security import pwd_context

load_dotenv()

def create_expertise(db: Session, data: ExpertiseBase):
    new_expertise = Expertise(
        name=data.name,
        description=data.description,
        img_url=[{"name": img.name, "url": img.url} for img in data.img_url]
    )

    db.add(new_expertise)
    db.commit()
    db.refresh(new_expertise)

    return new_expertise

def create_about(db: Session, about: AboutCreate):

    db_about = About(
        title=about.title,
        description=about.description,
        img_url=about.img_url
    )
    
    db.add(db_about)
    db.commit()
    db.refresh(db_about)
    
    return db_about

def get_abouts(db: Session):
    return db.query(About).all()

def create_admin_user(db: Session):
    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = os.getenv("ADMIN_PASSWORD")

    existing_admin = db.query(User).filter(User.username == admin_username).first()

    if not existing_admin:
        hashed_password = pwd_context.hash(admin_password)
        admin_user = User(username=admin_username, hashed_password=hashed_password, is_admin=True)
        db.add(admin_user)
        db.commit()
        print("Admin user created!")
    else:
        print("Admin user already exists.")

def create_category(db: Session, category: CategoryCreate):
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session):
    return db.query(Category).all()

def get_expertise(db: Session):
    return db.query(Expertise).all()

def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

def create_project(db: Session, project: ProjectCreate):
    db_project = Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get_projects(db: Session):
    return db.query(Project).all()

def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()

def delete_project(db: Session, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return None
    db.delete(project)
    db.commit()
    return project
