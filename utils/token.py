
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any
from jose import jwt, JWTError
from fastapi import HTTPException

ALGORITHM = "HS256"
# Load environment variables
load_dotenv()
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ACCESS_TOKEN_EXPIRE_MINUTES= int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
def create_access_token(data: dict, expires_delta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
def decode_jwt(token): 
    try:
        print("token", token)
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=ALGORITHM)
        return payload
    except JWTError as e:
        print(e)
        raise HTTPException(status_code=401, detail="Could not validate credentials")