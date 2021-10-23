from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional


class RazorData(BaseModel):
    razorpay_order_id:str
    razorpay_payment_id: str
    razorpay_signature: str
    error: Optional[bool] = False
