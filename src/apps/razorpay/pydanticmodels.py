from src.apps.razorpay.models import *
from tortoise.contrib.pydantic import pydantic_model_creator


Create_RazorPayment = pydantic_model_creator(
    RazorPayment, name="createrazorpayments", exclude=("id", "created", "updated", "payment_id", 'order_id'))
GET_RazorPayment = pydantic_model_creator(
    RazorPayment, name="razorpayments")
Create_MonthlyPlans = pydantic_model_creator(
    MonthlyPlans, name="craetemonthlyplans", exclude=("id", "created", "updated"))
GET_plans = pydantic_model_creator(
    MonthlyPlans, name="monthlyplans")



