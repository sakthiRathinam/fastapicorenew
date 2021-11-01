from uuid import uuid1, getnode
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
from .backgroundtask import *
import os
import shutil
from .service import *
from .schema import *
from .pydanticmodels import *
from fastapi_pagination import LimitOffsetPage, Page, add_pagination
from fastapi_pagination.ext.tortoise import paginate
import datetime
from src.apps.prescriptionapp.models import Clinic , ClinicZones , PharmacyOwners , ClinicReceponists , Prescription , Medicine
dunzo_router = APIRouter(dependencies=[Depends(get_current_login)])
from src.apps.razorpay.endpoints import client

async def background_alert(clinics):
    notificationIds = []
    for clinic in clinics:
        owners = await clinic.pharmacyownersusers.all()
        for owner in owners:
            user = await owner.user
            if user.notificationIds is not None:
                notificationIds.extend(user.notificationIds)

@dunzo_router.post('/createUserOrder')
async def create_user_orders(data: DunzoOrderSchema, task: BackgroundTasks):
    prescription = await Prescription.get(id=data.prescription)
    user = await User.get(id=data.user)
    order = CreateUserOrder.create(prescription=prescription, user=user, user_lat=data.lat, user_lang=data.lang, order_mode=data.order_mode, order_status="Pending")
    total_price = 0
    for medicine in data.medicines:
        medicine_obj = await Medicine.get(id=medicine.medicine)
        price = medicine_obj.max_retial_price * medicine.quantity
        total_price += price
        medicine_order = OrderMedicines.create(medicine=medicine_obj,medicine_time_id=medicine.medicine_time,price=price,quantity=medicine.quantity)
        await order.ordered_medicines.add(medicine_order)
    order.total_price =  total_price
    order.save()

    
@dunzo_router.post('/medicalOrder')
async def medical_accept(order: int = Body(...), clinic: int = Body(...), accepted_price: float = Body(...), all_available: Optional[bool] = True,accepted: Optional[bool] = True):
    # order_obj = await CreateUserOrder.get(id=order)
    # clinic_obj = await Clinic.get(id=clinic)
    medical_accept = await MedicalAccepted.create(medical_store_id=clinic, accepted_price=accepted_price, all_available=all_available,order_id=order)
    return medical_accept

@dunzo_router.get('/filterMedicalOrder')
async def medical_accept(limit: int = 10, offset: int = 0, status: Optional[MedicalAcceptStatus] = MedicalAcceptStatus.WAITING):
    # order_obj = await CreateUserOrder.get(id=order)
    # clinic_obj = await Clinic.get(id=clinic)
    medical_accept = await medical_accept.limited_data(offset,limit,status=status)
    return medical_accept


@dunzo_router.post('/createDunzoTask')
async def create_dunzo_task(medicalorder:int):
    medical_order = await MedicalAccepted.get(id=medicalorder).prefetch_related("medical_store","order")
    medical_order.status = "ACCEPTED"
    order = await medical_order.order
    medical_store = await medical_order.medical_store
    order.medical_store_id = medical_order.medical_store_id
    order.medical_lat = medical_store.lat
    order.medical_lang = medical_store.lang
    await order.save()
    await medical_store.save()
    user = await order.user
    data = {
        "request_id": str(uuid1(node=None, clock_seq=None)),
        "reference_id": str(uuid1(node=None, clock_seq=None)),
        "pick_details": [
            {
                "reference_id": str(uuid1(node=None, clock_seq=None)),
                "address": {
                    "lat": float(order.medical_lat),
                    "lng": float(order.medical_lang),
                    "street_address_1": medical_store.address,
                    "pincode": medical_store.pincode,
                    "contact_details": {
                        "name": medical_store.name,
                        "phone_number": medical_store.mobile
                    }
                }
            }
        ],
        "optimised_route": True,
        "drop_details": [
            {
                "reference_id": str(uuid1(node=None, clock_seq=None)),
                "address": {
                    "lat": float(order.user_lat),
                    "lng": float(order.user_lang),
                    "street_address_1": user.address,
                    "pincode": user.pincode,
                    "contact_details": {
                        "name": user.first_name + " "+user.last_name,
                        "phone_number": user.mobile
                    }
                },
            }
        ],
        "payment_method": "DUNZO_CREDIT",
    }
    letters = string.ascii_letters
    receipt = (''.join(random.choice(letters) for i in range(10)))
    DATA = {
        "amount": float(medical_order.accepted_price) * 100,
        "currency": 'INR',
        "receipt": receipt,
        "payment_capture": 1,
    }
    try:
        dunzo_order = DunzoOrder()
        dunzo_order.medical_store = order.accepted_store
        dunzo_order.user = order.user
        dunzo_order.to_send = json.dumps(data, indent=4)
        dunzo_order.order_id = c['id']
        dunzo_order.razor_price = DATA['amount']
        dunzo_order.main_order = medical_order
        dunzo_order.save()
        return JSONResponse({"order_id": dunzo_order.order_id, "success": "order was created succesfully", 'paymentpk': dunzo_order.id})
    except:
        return JSONResponse({"error": "same error occur while creating the order please try again"}, status_code=500)
    return JsonResponse({"error":"something went wrong please try again"})
    
    
@dunzo_router.post('/createDunzoTask')
async def create_dunzo_task(data: DunzoTask):
    url = "https://apis-staging.dunzo.in/api/v2/tasks"
    payment_verify = client.order.fetch(razorpay_order_id)
    params_dict = {
        'razorpay_order_id':data.razorpay_order_id,
        'razorpay_payment_id': data.razorpay_payment_id,
        'razorpay_signature': data.razorpay_signature,
    }
    client.utility.verify_payment_signature(params_dict)
    

    

    
@dunzo_router.post('/requestRefund')
async def request_refund(dunzoOrder: int = Body(...), status: Optional[MedicalAcceptStatus]=Body(...)):
    dunzo_order = await DunzoOrder.get(id=dunzoOrder)
    if status == 'CANCELLED':
        pass
    
        



    



    
    
    
            
        
        
                    




        
                    
            
                

                
        
        
        
    







