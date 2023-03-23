from fastapi import APIRouter, HTTPException, Depends,Request
from sqlalchemy.orm import Session
from typing import Optional
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
def getDevice(deviceId: int = None ,payload: dict = Depends(auth_middleware), db: Session = Depends(get_db)):
    devices = None
    if deviceId != None:
        devices = db.query(Device).filter(Device.id == deviceId).all()
    else :
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
    #special case just for tem device
    if updateBody.data_value != None:
        device.data_value = { 'tem': updateBody.data_value.tem, 'hum': updateBody.data_value.hum}
    db.commit()   
    print(f"Device after update: {device}")
    return {"message":"OK", "data": device}
@router.post('/devices')
def createDevice(createBody: CreateDevice, payload: dict = Depends(auth_middleware), db: Session = Depends(get_db)):
    data_value_json = None
    print(createBody)
    device = db.query(Device).filter(Device.name == createBody.name).first()
    if device:
        raise HTTPException(status_code=409, detail="Device name exist")
    if createBody.data_value != None:    
        data_value_json = {'tem': createBody.data_value.tem, 'hum': createBody.data_value.hum}
    newDevice = Device(name=createBody.name, type=createBody.type, data_value=data_value_json)
    db.add(newDevice)
    db.commit()   
    return {"message":"OK"}    
@router.delete('/devices/{deviceId}')
def deleteDevice(deviceId: int, payload: dict = Depends(auth_middleware), db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.id == deviceId).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    db.delete(device)
    db.commit()
    return { "message": "OK"}