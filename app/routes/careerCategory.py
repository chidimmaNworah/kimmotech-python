from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import CareerCategory
from ..schemas import CareerCategoryResponse, CareerCategoryCreate, CareerCategoryBase

router = APIRouter()

@router.post("/career-categories/", response_model=CareerCategoryResponse)
def add_career_category(category: CareerCategoryCreate, db: Session = Depends(get_db)):
    """Add a new career category."""
    existing_category = db.query(CareerCategory).filter(CareerCategory.name == category.name).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Career category already exists")

    new_category = CareerCategory(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.get("/career-categories/", response_model=list[CareerCategoryResponse])
def list_career_categories(db: Session = Depends(get_db)):
    """Fetch all career categories."""
    return db.query(CareerCategory).all()

@router.get("/career-categories/{category_id}", response_model=CareerCategoryResponse)
def fetch_career_category(category_id: int, db: Session = Depends(get_db)):
    """Fetch a specific career category by ID."""
    category = db.query(CareerCategory).filter(CareerCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Career Category not found")
    return category
