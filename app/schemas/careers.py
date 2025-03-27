from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CareerResponse(BaseModel):
    id: int
    title: str
    slug: str
    excerpt: str
    description: str
    industry: Optional[str] = None
    field: Optional[List[str]] = None
    state: Optional[str] = None
    region: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    category_id: int

    class Config:
        from_attributes = True

class CareerDelete(BaseModel):
    message: str
