from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.models import User
from database.database import SessionLocal, get_db
from passlib.context import CryptContext
from dto.user import UserAuth
from utils.token import create_access_token
router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login")
def login(userBody: UserAuth, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == userBody.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not pwd_context.verify(userBody.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    access_token = create_access_token(data = { "sub": str(user.id)} )
    return {"msg": "Successfully authenticated", "access_token": access_token}
