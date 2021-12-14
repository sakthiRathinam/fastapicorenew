from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional
from fastapi import UploadFile, File
from datetime import date, datetime, time, timedelta
from .models import OrderType, DunzoState, DunzoPayments, PaymentStatus, OrderState

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
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    
class RequestRefund(BaseModel):
    order:int
    status: DunzoState

class CartItem(BaseModel):
    medicine_id:int
    medicine_name:str
    medicine_type:str
    quantity:int
    price:float
    
class Checkout(BaseModel):
    user_id:int
    medical_store_id:int
    cart_items:List[CartItem]
    lat: float
    km: float
    lang: float
    total_price: float
    prescription: Optional[int] = None
    order_mode: OrderState
    address: str
    pincode: str
    landmark: str
    
    
