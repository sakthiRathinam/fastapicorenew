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


    


    
    
    
    
            
        
        
                    




        
                    
            
                

                
        
        
        
    







