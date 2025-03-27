from pydantic import BaseModel

class CareerCategoryBase(BaseModel):
    name: str

class CareerCategoryCreate(CareerCategoryBase):
    pass

class CareerCategoryResponse(CareerCategoryBase):
    id: int

    class Config:
        form_attributes = True
