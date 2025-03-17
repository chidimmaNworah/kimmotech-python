from fastapi import FastAPI, UploadFile, Form
from pydantic import BaseModel
from typing import List

class ImageData(BaseModel):
    name: str
    url: str

class ExpertiseBase(BaseModel):
    name: str
    description: str
    img_url: List[ImageData]

class ExpertiseResponse(BaseModel):
    id: int
    name: str
    description: str
    img_url: List[ImageData]

    class Config:
        from_attributes = True