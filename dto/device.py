from pydantic import BaseModel
from typing import Optional, Union
class Data_value(BaseModel):
    tem: float
    hum: float 
class UpdateDevice(BaseModel):
    status: Optional[bool]
    name: Optional[str]
    data_value: Union[Data_value, None]
class CreateDevice(BaseModel):
    name: str  
    type: int
    data_value: Union[Data_value, None]
