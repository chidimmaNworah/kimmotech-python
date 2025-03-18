import os
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .database import engine, Base, SessionLocal
from .crud import create_about, get_abouts, create_admin_user
from .routes import auth, users, about, category, project, expertise, jobs, newsletter
from dotenv import load_dotenv
import cloudinary.uploader

load_dotenv()

# Cloudinary configuration
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users && Messages && Comments"])
app.include_router(about.router, prefix="/about", tags=["About"])
app.include_router(category.router, prefix="/category", tags=["Category"])
app.include_router(project.router, prefix="/project", tags=["Projects"])
app.include_router(expertise.router, prefix="/expertise", tags=["Expertise"])
app.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
app.include_router(newsletter.router, prefix="/jobs", tags=["Jobs/newsletters"])


Base.metadata.create_all(bind=engine)

db = SessionLocal()
create_admin_user(db)
db.close()

@app.get("/")
def home():
    return {"message": "FastAPI is running!"}