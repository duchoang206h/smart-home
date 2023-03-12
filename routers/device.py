from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.models import Device
from database.database import SessionLocal, get_db
from passlib.context import CryptContext
import json
from dto.user import UserAuth
from dto.device import UpdateDevice, CreateDevice
from utils.device import DEVICE_TYPE
from utils.token import create_access_token
from middlewares.auth import auth_middleware

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/devices")
def getDevice(payload: dict = Depends(auth_middleware), db: Session = Depends(get_db)):
    devices = db.query(Device).all()
    return {"data": devices}
@router.get("/devices/type")
def getDeviceType():
    deviceTypeDict = {d.name: d.value for d in DEVICE_TYPE}

    return {"data": deviceTypeDict}    
@router.put('/devices/{deviceId}')
def updateDevice(deviceId: int, updateBody: UpdateDevice, payload: dict = Depends(auth_middleware), db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.id == deviceId).first()
    print(f"Device before update: {device}")
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    if updateBody.status != None:
        device.status = updateBody.status    
    if updateBody.name != None:
        device.name = updateBody.name
    db.commit()   
    print(f"Device after update: {device}")
    return {"message":"OK", "data": device}
@router.post('/devices')
def createDevice(createBody: CreateDevice, payload: dict = Depends(auth_middleware), db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.name == createBody.name).first()
    print(createBody)
    if device:
        raise HTTPException(status_code=409, detail="Device name exist")
    newDevice = Device(name=createBody.name, type=createBody.type)
    db.add(newDevice)
    db.commit()   
    return {"message":"OK"}    