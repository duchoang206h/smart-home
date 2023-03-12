from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from database.database import SessionLocal, get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import json
from utils.token import create_access_token
from middlewares.auth import auth_middleware

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/recognize")
def recognize(sound: UploadFile = File(...), db: Session = Depends(get_db)):
    #wait for recognize
    return {"data": sound.filename}
