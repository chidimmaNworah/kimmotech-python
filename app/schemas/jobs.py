from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class JobBase(BaseModel):
    title: str
    excerpt: str
    description: str
    categories: List[str]
    industry: str
    field: List[str]
    state: str
    region: str
    slug: Optional[str] = None  # Auto-generated if not provided


class JobCreate(JobBase):
    pass

class JobResponse(JobBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        form_attributes = True

class JobDelete(BaseModel):
    message: str
