from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional
from .models import RazorPayPlans

class RazorData(BaseModel):
    razorpay_order_id:str
    razorpay_payment_id: str
    razorpay_signature: str
    error: Optional[bool] = False


class CreateMonthlyPlan(BaseModel):
    amount: int
    title: str
    discount_percent: Optional[int] = 0
    number_of_months: Optional[int] = 1


class CreateRazorPayment(BaseModel):
    clinic_id: int
    user_id:int
    selected_plan:int
    
    
    
