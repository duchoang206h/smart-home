from sqlalchemy import Column, Integer, String, Boolean, Float
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String)
class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), unique=True, index=True)
    type = Column(String(50))
    status= Column(Boolean, default=False)
    data_value = Column(Float)
