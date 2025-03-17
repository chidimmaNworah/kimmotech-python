from fastapi import APIRouter, Depends, HTTPException, Form
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Newsletter
from ..schemas import NewsletterCreate, NewsletterResponse

router = APIRouter()

@router.post("/newsletter/")
async def subscribe_newsletter(
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        existing_subscription = db.query(Newsletter).filter(Newsletter.email == email).first()
        if existing_subscription:
            raise HTTPException(status_code=400, detail="Email is already subscribed.")

        new_newsletter = Newsletter(
            email=email,
            platform="careers"
        )

        db.add(new_newsletter)
        db.commit()
        db.refresh(new_newsletter)

        return {"message": "Successfully subscribed!", "email": new_newsletter.email}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/newsletter/", response_model=list[NewsletterResponse])
def list_newsletter(db: Session = Depends(get_db)):
    return db.query(Newsletter).all()

@router.delete("/newsletter/unsubscribe/")
async def unsubscribe_newsletter(email: str, db: Session = Depends(get_db)):
    try:
        subscription = db.query(Newsletter).filter(Newsletter.email == email).first()
        if not subscription:
            raise HTTPException(status_code=404, detail="Email not found in subscriptions.")

        db.delete(subscription)
        db.commit()
        return {"message": "Successfully unsubscribed!"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
    # https://yourwebsite.com/newsletter/unsubscribe?email=user@example.com
