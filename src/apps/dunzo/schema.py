from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional
from fastapi import UploadFile, File
from datetime import date, datetime, time, timedelta
from .models import OrderType

class OrderMedicines(BaseModel):
    medicine:int
    quantity:int
    medicine_time:int
    
class DunzoOrderSchema(BaseModel):
    user_lat:str
    user_lang: str
    prescription: int
    neary_by:Optional[bool] = None
    zone:Optional[str] = None
    medicines: List[OrderMedicines]
    order_mode: OrderType
    lat:str
    lang:str


class DunzoTask(BaseModel):
    dunzo_order : int
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    
