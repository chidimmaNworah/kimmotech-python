from fastapi import FastAPI, HTTPException, Body, Path
from pydantic import BaseModel
from typing import Optional

class AboutCreate(BaseModel):
    title: str
    description: str
    img_url: Optional[str]

class AboutResponse(AboutCreate):
    id: int

    class Config:
        form_attributes = True