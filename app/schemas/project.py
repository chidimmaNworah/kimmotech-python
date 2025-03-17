from fastapi import FastAPI, HTTPException, Body, Path
from pydantic import BaseModel
from typing import Optional
from ..schemas import CategoryResponse

class ProjectBase(BaseModel):
    title: str
    description: str
    github_link: str | None = None
    preview_link: str | None = None
    img_url: str
    category_id: int  # Ensure this is passed when creating a project

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    category: CategoryResponse  # To return category details in response

class Config:
        form_attributes = True

class ProjectDelete(BaseModel):
    message: str