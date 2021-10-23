
import uuid
from starlette.responses import JSONResponse
# from starlette.requests import Request
from src.apps.users.models import User
from starlette import status
from .models import *
from src.config.settings import BASE_DIR, STATIC_ROOT, MEDIA_ROOT
from src.apps.users.views import get_current_login
from src.apps.base.service_base import CustomPage
from fastapi import APIRouter, Depends, BackgroundTasks, Response, status, Request, File, UploadFile, Body
from tortoise.query_utils import Q
import pathlib
from typing import List, Optional
from src.apps.users.models import User, User_Pydantic
from src.apps.users.service import user_service
import os
import shutil
from .service import *
from .schema import *
from .pydanticmodels import *
from fastapi_pagination import LimitOffsetPage, Page, add_pagination
from fastapi_pagination.ext.tortoise import paginate
import datetime
import string
import razorpay

from src.config.settings import RAZOR_API_KEY,RAZOR_SECRET_KEY

client = razorpay.Client(auth=(RAZOR_API_KEY,RAZOR_SECRET_KEY))
client.set_app_details({"title":"fastapi","version":"0.1.16"})
razor_router = APIRouter()

clinto_subscription_map = {
    "Monthly":499,
    "Quarterly": 1399,
    "Halfly": 2799,
    "Yearly": 5499,
}
@razor_router.post('/addPayment')
async def add_medicines(data: Create_RazorPayment = Body(...),clinic:int = Body(...),user:int = Body(...)):
    pay = await RazorPayment.create(clinic_id=clinic, user_id=user, **data.dict(exclude_unset=True))
    letters = string.ascii_letters
    receipt = (''.join(random.choice(letters) for i in range(10)))
    clinic_obj = await Clinic.get(id=clinic).prefetch_related('clinicpayments')
    # start_date = await
    start_date = datetime.date.today()
    subscription_exists = await clinic_obj.clinicsubscriptions.filter(valid_till__gte=end_date, status='Success',active=True).order_by('-valid_till')
    if len(subscription_exists) > 0:
        latest_subscription = subscription_exists[0]
        start_date = latest_subscription.valid_till
    if 'subscription' in data:
        DATA = {
            "amount": clinto_subscription_map[data.subscription],
            "currency": 'INR',
            "receipt": receipt,
            "payment_capture": 1,
        }
        days = datetime.timedelta(days=28)
        end_date = start_date + days
        try:
            c = client.order.create(data=DATA)
            pay.order_id = c['id']
            pay.amount = DATA['amount']
            pay.subscription_date = start_date
            pay.valid_till = end_date
            await pay.save()
            return JSONResponse({"order_id": pay.order_id, "success": "order was created succesfully", 'paymentpk': pay.id},status_code=200)
        except:
            return JSONResponse({"error": "same error occur while creating the order please try again"}, status_code=500)
    return JSONResponse({"error": "kindly enter all the required info"}, status_code=500)


@razor_router.post('/validatePayment')
async def validate_payment(data: RazorData):
    if not data.error:
        try:
            c = client.order.fetch(data.razorpay_order_id)
            params_dict = {
                'razorpay_order_id': data.razorpay_order_id,
                'razorpay_payment_id': data.razorpay_payment_id,
                'razorpay_signature': data.razorpay_signature,
            }
            client.utility.verify_payment_signature(params_dict)
            if c['amount_due'] == 0:
                p = await RazorPayment.get(order_id=data.razorpay_order_id)
                p.payment_id = data.razorpay_payment_id
                p.status = 'Success'
                p.save()
                return JSONResponse({"success": "your plan is activated now"})
        except:
            return JSONResponse({"failed": "payment failed try again"}, status_code=500)
    else:
        return JSONResponse({"failed": "something went wrong please try again"}, status_code=500)
        

@razor_router.post('/refundPayment')
async def refund_payment(payment:int):
    razor_payment = await RazorPayment.get(id=payment)
    if razor_payment.status == 'Success':
        try:
            refund = client.payment.refund(
                razor_payment.payment_id, round(razor_payment.amount))
        except:
            return JSONResponse({"failed": "razor server error try again"}, status_code=500)
        razor_payment.status = "Refunded"
        razor_payment.active = False
        razor_payment.is_refunded = False
        razor_payment.save()
        return JSONResponse({"success": "razorpay amount sended successfully"}, status_code=200)
    return JSONResponse({"error":"please enter the required info"},status_code=500)



        
    
@razor_router.delete('/deletePayments')
async def delete_payments(id: int):
    await razor_pay.delete(id=id)
    return {"success": "deleted"}


@razor_router.put('/updatePayments')
async def update_payments(id: int, data: Create_RazorPayment = Body(...)):
    await razor_pay.update(data, id=id)
    return {"success": "updated"}


@razor_router.get('/filterPayments')
async def filter_payments(data: Create_RazorPayment = Body(...)):
    await razor_pay.filter(**data.dict(exclude_unset=True))
    return {"success": "updated"}
