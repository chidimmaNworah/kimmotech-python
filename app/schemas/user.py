from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class CommentBase(BaseModel):
    career_id: int
    name: str
    email: EmailStr
    content: str

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    created_at: datetime
    career_id: int

    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    name: str
    email: EmailStr
    message: str

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    email: EmailStr
    created_at: datetime
    comments: List[CommentResponse] = []
    messages_sent: List[MessageResponse] = []

    class Config:
        from_attributes = True