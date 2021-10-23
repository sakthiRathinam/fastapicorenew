from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional


class inner_data(BaseModel):
    pk:int
    message:  Optional[str] = None
    thread : int
    msgType: Optional[str] = None
    senderPk: Optional[str] = None
    senderFirstName: Optional[str] = None
    senderLastName: Optional[str] = None
    attachment: Optional[str] = None
    created: str
    
    
class Send_Data(BaseModel):
    topic : str
    args: List[inner_data]
