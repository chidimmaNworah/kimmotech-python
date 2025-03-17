from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import List
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader
from ..database import get_db
from ..models import Expertise
from ..schemas import ExpertiseBase, ExpertiseResponse
from ..crud import get_expertise, create_expertise

router = APIRouter()

@router.post("/expertise/")
async def add_expertise(
    name: str = Form(...),
    description: str = Form(...),
    images: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    try:
        uploaded_images = []
        
        for image in images:
            upload_result = cloudinary.uploader.upload(
                image.file, 
                folder="kimmotech/expertise"
            )
            uploaded_images.append({"name": image.filename, "url": upload_result["secure_url"]})

        # Create the expertise object
        new_expertise = Expertise(
            name=name,
            description=description,
            img_url=uploaded_images
        )

        # Save to database
        db.add(new_expertise)
        db.commit()
        db.refresh(new_expertise)

        return new_expertise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/expertise/", response_model=list[ExpertiseResponse])
def list_expertise(db: Session = Depends(get_db)):
    return get_expertise(db)