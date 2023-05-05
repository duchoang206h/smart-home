from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from database.database import SessionLocal, get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import json
from database.models import Device

from utils.token import create_access_token
from utils.status import getPkFromKeyword, getStatusFromKeyword
from middlewares.auth import auth_middleware
from recognize.keyword_spotting_service import recognize_voice
router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/recognize")
def recognize(sound: bytes = File(...) , db: Session = Depends(get_db)):
    #wait for recognize
    keyword = recognize_voice(sound)
    print(keyword)
    status = getStatusFromKeyword(keyword)
    pk = getPkFromKeyword(keyword)
    search = "%{}%".format(pk)
    device = db.query(Device).filter(Device.name.like(search)).first()
    if device != None:
        device.status = status
        response = Device(id=device.id, name=device.name, type=device.type, data_value=device.data_value, status=device.status)
    else:
        response = None
    db.commit()
    return {"data": keyword, "status": status, "pk": pk, "device": response}
