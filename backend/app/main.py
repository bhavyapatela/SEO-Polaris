from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.app.core.config import settings
from backend.app.core.db import engine, Base, get_db
from backend.app.models import models

# Auto-initialize database tables locally
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "api_v1_docs": "/docs"
    }

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # Check database connectivity
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception:
        db_status = "unreachable"
    return {
        "status": "healthy",
        "database": db_status
    }
