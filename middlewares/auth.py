from fastapi import Header, HTTPException
from jose import  JWTError
from utils.token import decode_jwt

async def auth_middleware(authorization: str = Header(...)):
    try:
        print(authorization)
        scheme, token = authorization.split()
        print(token)
        print(scheme)
        payload = decode_jwt(token)
        return payload
    except JWTError as e:
        print(e)
        raise HTTPException(status_code=401, detail='Invalid access token')
