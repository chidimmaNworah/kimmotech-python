from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Message, Comment
from ..schemas import UserCreate, MessageResponse, MessageBase, MessageCreate, CommentBase, CommentCreate, CommentResponse
from ..utils.security import pwd_context, create_access_token
from datetime import timedelta

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


SECRET_KEY = "blackblackblacksheephaveyouanywool"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = pwd_context.hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = get_user_by_username(db, form_data.username)
        if not user or not pwd_context.verify(form_data.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Invalid username or password")
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        print(f"Login Error: {e}")  # Log the actual error
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post("/messages", response_model=MessageResponse)
def create_message(messages: MessageCreate, db: Session = Depends(get_db)):
    new_message = Message(
        name=messages.name,
        email=messages.email,
        message=messages.message
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

@router.get("/messages", response_model=List[MessageResponse])
def get_messages(db: Session = Depends(get_db)):
    messages = db.query(Message).all()
    return messages

@router.post("/comments", response_model=CommentResponse)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    new_comment = Comment(
        career_id=comment.career_id,
        name=comment.name,
        email=comment.email,
        content=comment.content
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.get("/comments/{career_id}", response_model=List[CommentResponse])
def get_comments(career_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.career_id == career_id).all()
    return comments  # ✅ Always returns a list (empty or filled)