from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List
from slugify import slugify

from ..database import get_db
from ..models import Career
from ..schemas import CareerResponse, CareerDelete

router = APIRouter()

@router.post("/careers/", response_model=CareerResponse)
def add_career(
    title: str = Form(...),
    excerpt: str = Form(...),
    description: str = Form(...),
    industry: str = Form(None),
    field: str = Form(None),
    state: str = Form(None),
    region: str = Form(None),
    category_id: int = Form(...),
    db: Session = Depends(get_db)
):
    field_list = field.split(",") if field else None
    slug = slugify(title)

    existing_career = db.query(Career).filter(Career.slug == slug).first()
    if existing_career:
        raise HTTPException(status_code=400, detail="Career with this title already exists.")

    new_career = Career(
        title=title,
        slug=slug,
        excerpt=excerpt,
        description=description,
        industry=industry,
        field=field_list,
        state=state,
        region=region,
        category_id=category_id
    )

    db.add(new_career)
    db.commit()
    db.refresh(new_career)
    return new_career

@router.get("/careers/", response_model=List[CareerResponse])
def list_careers(db: Session = Depends(get_db)):
    print(list_careers)
    return db.query(Career).all()

@router.get("/careers/{career_id}", response_model=CareerResponse)
def get_career_detail(career_id: int, db: Session = Depends(get_db)):
    career = db.query(Career).filter(Career.id == career_id).first()
    if not career:
        raise HTTPException(status_code=404, detail="Career not found")
    return career

@router.delete("/careers/{career_id}", response_model=CareerDelete)
def delete_career(career_id: int, db: Session = Depends(get_db)):
    career = db.query(Career).filter(Career.id == career_id).first()
    if not career:
        raise HTTPException(status_code=404, detail="Career not found")
    db.delete(career)
    db.commit()
    return {"message": "Career deleted successfully"}
