from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session
import cloudinary.uploader
from ..database import get_db
from ..models import Project, Category
from ..schemas import ProjectCreate, ProjectResponse, ProjectDelete
from ..crud import create_project,get_project, get_projects

router = APIRouter()

@router.post("/projects/", response_model=ProjectResponse)
async def add_project(title: str = Form(...), description: str = Form(...), github_link: str = Form(...), preview_link: str = Form(...), file: UploadFile = File(...), category_id: int = Form(...), db: Session = Depends(get_db)):

    image_file = await file.read()
    upload_result = cloudinary.uploader.upload(image_file)
    img_url = upload_result["secure_url"]

    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Invalid category")
    
    project_data = ProjectCreate(title=title, description=description,github_link=github_link, preview_link=preview_link, img_url=img_url, category_id=category_id)

    return create_project(db, project_data)

@router.get("/projects/", response_model=list[ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    return get_projects(db)

@router.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project_detail(project_id: int, db: Session = Depends(get_db)):
    project = get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.delete("/projects/{project_id}", response_model=ProjectDelete)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}
