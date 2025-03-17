from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Job
from ..schemas import JobResponse, JobDelete
from typing import List
from slugify import slugify

router = APIRouter()

@router.post("/jobs/", response_model=JobResponse)
def add_job(
    title: str = Form(...),
    excerpt: str = Form(...),
    description: str = Form(...),
    industry: str = Form(None),
    field: str = Form(None),
    state: str = Form(None),
    region: str = Form(None),
    categories: str = Form(...),
    db: Session = Depends(get_db)
):
    category_list = categories.split(",")
    field_list = field.split(",")
    slug = slugify(title)

    existing_job = db.query(Job).filter(Job.slug == slug).first()
    if existing_job:
        raise HTTPException(status_code=400, detail="Job with this title already exists.")

    new_job = Job(
        title=title,
        slug=slug,
        excerpt=excerpt,
        description=description,
        industry=industry,
        field=field_list,
        state=state,
        region=region,
        categories=category_list
        )
    
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@router.get("/jobs/", response_model=List[JobResponse])
def list_jobs(db: Session = Depends(get_db)):
    return db.query(Job).all()

@router.get("/jobs/{job_id}", response_model=JobResponse)
def get_job_detail(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.delete("/jobs/{job_id}", response_model=JobDelete)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return {"message": "Job deleted successfully"}
