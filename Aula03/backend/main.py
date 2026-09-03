from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "sqlite:///./images.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    content_type = Column(String)
    image_data = Column(LargeBinary)
    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    contents = await file.read()
    
    db = SessionLocal()
    try:
        db_image = Image(
            filename=file.filename,
            content_type=file.content_type,
            image_data=contents
        )
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        return {
            "id": db_image.id,
            "filename": db_image.filename,
            "content_type": db_image.content_type,
            "created_at": db_image.created_at.isoformat()
        }
    finally:
        db.close()


@app.get("/images")
async def list_images():
    db = SessionLocal()
    try:
        images = db.query(Image).all()
        return [
            {
                "id": img.id,
                "filename": img.filename,
                "content_type": img.content_type,
                "created_at": img.created_at.isoformat()
            }
            for img in images
        ]
    finally:
        db.close()


@app.get("/images/{image_id}")
async def get_image(image_id: int):
    db = SessionLocal()
    try:
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        
        return StreamingResponse(
            io.BytesIO(image.image_data),
            media_type=image.content_type
        )
    finally:
        db.close()


@app.delete("/images/{image_id}")
async def delete_image(image_id: int):
    db = SessionLocal()
    try:
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        
        db.delete(image)
        db.commit()
        return {"message": "Image deleted successfully"}
    finally:
        db.close()
