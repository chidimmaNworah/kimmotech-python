from pydantic import BaseModel

class NewsletterBase(BaseModel):
    email: str
    platform: str

class NewsletterCreate(NewsletterBase):
    pass

class NewsletterResponse(NewsletterBase):
    id: int

    class Config:
        form_attributes = True
