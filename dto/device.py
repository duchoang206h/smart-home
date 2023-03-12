from pydantic import BaseModel
from typing import Optional
class UpdateDevice(BaseModel):
    status: Optional[bool]
    name: Optional[str]
class CreateDevice(BaseModel):
    name: str  
    type: int
