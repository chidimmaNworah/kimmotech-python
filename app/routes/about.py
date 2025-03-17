from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from sqlalchemy.orm import Session
import cloudinary.uploader
from ..database import get_db
from ..models import About
from ..schemas import AboutCreate, AboutResponse
from ..crud import create_about, get_abouts, create_admin_user

router = APIRouter()

@router.post("/abouts/", response_model=AboutResponse)
async def add_about(
    title: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    image_file = await file.read()
    
    upload_result = cloudinary.uploader.upload(image_file)
    img_url = upload_result["secure_url"]

    about_data = AboutCreate(title=title, description=description, img_url=img_url)
    
    return create_about(db, about_data)

@router.get("/abouts/", response_model=list[AboutResponse])
def list_abouts(db: Session = Depends(get_db)):
    return get_abouts(db)

@router.get("/abouts/{about_id}", response_model=AboutResponse)
async def get_about(about_id: int, db: Session = Depends(get_db)):
    about = db.query(About).filter(About.id == about_id).first()
    if not about:
        raise HTTPException(status_code=404, detail="About not found")
    return about

@router.put("/abouts/{about_id}", response_model=AboutResponse)
async def update_about(
    about_id: int,
    title: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    # Find the about by id
    about = db.query(About).filter(About.id == about_id).first()

    if not about:
        raise HTTPException(status_code=404, detail="About not found")
    
    # Update title and description
    about.title = title
    about.description = description
    
    # Update the image if a new one is provided
    if file:
        image_file = await file.read()
        upload_result = cloudinary.uploader.upload(image_file)
        about.img_url = upload_result["secure_url"]

    db.commit()
    db.refresh(about)
    return about

@router.delete("/abouts/{about_id}")
def delete_about(about_id: int, db: Session = Depends(get_db)):
    about = db.query(About).filter(About.id == about_id).first()
    if not about:
        raise HTTPException(status_code=404, detail="About not found")
    db.delete(about)
    db.commit()
    return {"message": "About deleted successfully"}
