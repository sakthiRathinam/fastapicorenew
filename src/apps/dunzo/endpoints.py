import aiohttp
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
from src.apps.prescriptionapp.endpoints import age
from fastapi_pagination import LimitOffsetPage, Page, add_pagination
from fastapi_pagination.ext.tortoise import paginate
import datetime
import asyncio
from src.apps.users.models import User
from src.apps.prescriptionapp.models import Clinic , ClinicZones , PharmacyOwners , ClinicReceponists , Prescription , Medicine
dunzo_router = APIRouter(dependencies=[Depends(get_current_login)])
from src.apps.razorpay.endpoints import client
from src.config.settings import DUNZO_HEADERS as headers
from src.config.settings import DUNZO_URL as url
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

import math
@dunzo_router.post('/dunzoMedicalAccept')
async def dunzo_medical_accept(cart: int):
    cart = await Cart.get(id=cart)
    dunzo_orders = await cart.cartdunzoorders.all().order_by('-created')
    if len(dunzo_orders) > 0:
        p = dunzo_orders[0]
    else:
        return JSONResponse({"failed":"something went wrong"},status_code=500)
    print("heree")
    print(p.to_send)
    data = p.to_send
    print(data)
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url, json=data) as dunzo_order:
            if dunzo_order.status == 201:

                json_format = await dunzo_order.json()
                json_format = await dunzo_order.json()
                print(json_format)
                p.estimated_price = json_format["estimated_price"]
                p.task_id = json_format["task_id"]
                p.razor_commision = math.ceil(
                    p.razor_price * 2 / 100)
                cart.order_status = "Accepted"
                await cart.save()
                await p.save()
    return JSONResponse({"dunzo": "amount refunded", "success": json_format}, status_code=200)
    if dunzo_order.status != 201:
        try:
            refund = client.payment.refund(
                params['razorpay_payment_id'], round(p.razor_price))
            p.is_refunded = True
            p.is_cancelled = True
            p.refund_id = refund['id']
            await p.save()
            return JSONResponse({"dunzoerror": "amount refunded", "error": await dunzo_order.content}, status_code=500)
        except:
            p.is_cancelled = True
            await p.save()
            return JSONResponse({"paymenterror": "try again amount is not refunded", "error": await dunzo_order.content}, status_code=500)


    
    
@dunzo_router.post('/validateDunzoTask')
async def create_dunzo_task(data: DunzoTask,background_tasks:BackgroundTasks):
    dunzo_order = await DunzoOrder.get(
        order_id=data.razorpay_order_id)
    payment_verify = client.order.fetch(data.razorpay_order_id)
    medical_store = await dunzo_order.medical_store
    owner_objs = await medical_store.pharmacyownersusers.all()
    if len(owner_objs) > 0:
        owner = await owner_objs[0].user
    user_obj = await dunzo_order.user
    params_dict = {
        'razorpay_order_id':data.razorpay_order_id,
        'razorpay_payment_id': data.razorpay_payment_id,
        'razorpay_signature': data.razorpay_signature,
    }
    client.utility.verify_payment_signature(params_dict)
    c = client.order.fetch(data.razorpay_order_id)
    if c['amount_due'] == 0:
        dunzo_order.payment_id = data.razorpay_order_id
        dunzo_order.payment_status = 'Success'
        dunzo_order.is_received = True
        await dunzo_order.save()
        cart = await dunzo_order.cart
        cart.order_status = "Pending"
        await cart.save()
        background_tasks.add_task(
            notify_dunzo_order, dunzo_order.cart_id, dunzo_order.id, owner.notificationIds, user_obj.notificationIds)
        return JSONResponse({"success": "payment successfully paid","cartid":dunzo_order.cart_id})
    

@dunzo_router.post('/requestRefund')
async def request_refund(data: DunzoTask):
    data = data.dict()
    p = await DunzoOrder.get(id=data.order_id)
    if data['status'] == 'cancelled':
        if p.is_cancelled and not p.is_refunded and p.is_received:
            refund = client.payment.refund(
                p.payment_id, round(p.razor_price))
            p.is_refunded = True
            p.is_cancelled = True
            p.refund_id = refund['id']
            p.save()
            return JSONResponse({"success": "money refunded successfully"})
        else:
            return JSONResponse({"error":"error money already refunded"},status_code=500)
    else:
        if p.is_received and not p.is_refunded:
            try:
                refund = client.payment.refund(
                    p.payment_id, round(p.razor_price))
            except:
                return Response({"error": "money refunded successfuily"})
            p.is_refunded = True
            p.is_cancelled = True
            p.refund_id = refund['id']
            p.save()
            return JSONResponse({"success": "money refunded successfuily"})
        else:
            return JSONResponse({"error": "money refunded already"}, status=500)
import string
import random
import json
@dunzo_router.post('/checkoutCart')
async def request_refund(data: Checkout, background_tasks: BackgroundTasks):
    data_dict = data.dict()
    cart_items = data_dict.pop('cart_items')
    medical_store = await Clinic.get(id=data.medical_store_id)
    owner_objs = await medical_store.pharmacyownersusers.all()
    if len(owner_objs) > 0:
        owner = await owner_objs[0].user
    user_obj = await User.get(id=data.user_id)
    if data_dict['order_mode'] == "Instore":
        if data.km > medical_store.instore_pickup_kms:
            return JSONResponse({"failed": "this one is out of the medical store instore radius"},status_code=500)
    if data_dict['prescription'] is not None:
        data_dict['prescription_id'] = data_dict.pop('prescription')
    if data_dict['order_mode'] == 'Dunzo':
        data_dict['order_status'] = 'PaymentWaiting'
    cart =await Cart.create(**data_dict)
    for medicine in cart_items:
        cart_item = await CartSubs.create(**medicine, cart_id=cart.id)
    if data_dict['order_mode'] == "Dunzo":
        user_obj = await cart.user
        dunzo_order = DunzoOrder()
        dunzo_order.cart_id = cart.id
        dunzo_order.amount = cart.total_price
        data = {
            "request_id": str(uuid1(node=None, clock_seq=None)),
            "reference_id": str(uuid1(node=None, clock_seq=None)),
            "pickup_details": [
                {
                    "reference_id": str(uuid1(node=None, clock_seq=None)),
                    "address": {
                        "lat": float(medical_store.lat),
                        "lng": float(medical_store.lang),
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
                        "lat": float(cart.lat),
                        "lng": float(cart.lang),
                        "street_address_1": user_obj.address,
                        "pincode": user_obj.pincode,
                        "contact_details": {
                            "name": user_obj.first_name + " "+user_obj.last_name,
                            "phone_number": user_obj.mobile
                        }
                    },
                }
            ],
            "payment_method": "DUNZO_CREDIT",
        }
        letters = string.ascii_letters
        receipt = (''.join(random.choice(letters) for i in range(10)))
        DATA = {
            "amount": float(cart.total_price) * 100,
            "currency": 'INR',
            "receipt": receipt,
            "payment_capture": 1,
        }
        try:
            c = client.order.create(data=DATA)
            dunzo_order.medical_store = medical_store
            dunzo_order.user = user_obj
            print(data)
            # dunzo_order.to_send = json.dumps(data, indent=4)
            dunzo_order.to_send = data
            print(dunzo_order.to_send)
            dunzo_order.order_id = c['id']
            dunzo_order.razor_price = DATA['amount']
            await dunzo_order.save()
            
            return JSONResponse({"order_id": dunzo_order.order_id, "success": "order was created succesfully", 'paymentpk': dunzo_order.id})
        except:
            return JSONResponse({"error": "same error occur while creating the order please try again"}, status_code=500)
        return JsonResponse({"error": "something went wrong please try again"})
    background_tasks.add_task(
        notify_cancel_order, cart.id,owner.notificationIds, user_obj.notificationIds)
    return "cart created successfully"
        
from datetime import date,datetime
@dunzo_router.get('/getCarts')
async def get_carts(medical: Optional[int]=None,user:Optional[int]=None, status: Optional[OrderStatus] = None, limit: Optional[int] = 0, offset: Optional[int] = 0, date: Optional[date] = None):
    data_dict = dict()
    if medical is not None:
        data_dict['medical_store_id'] = medical
    if user is not None:
        data_dict['user_id'] = user
    if status is not None:
        if status == 'Accepted' or status == "Declined":
            data_dict['order_status__in'] = ['Accepted','Declined']
        else:
            data_dict['order_status'] = status
    if date is not None:
        data_dict['created__istartswith'] = date
    get_carts = await cart_view.limited_data(limit=limit, offset=offset, **data_dict)
    cart_data = []
    print(get_carts)
    for cart in get_carts['data']:
        cartsubs = await cart.cartsubmedicines.all()
        user_data = await cart.user
        default_address = await user_data.useraddresses.filter(default=True)
        clinic = await cart.medical_store
        data = {"maindata": cart, "submedicines": cartsubs, "user": {"name": user_data.first_name + " " + user_data.last_name, "id": user_data.id, "age": age(
            user_data.date_of_birth), "dob": user_data.date_of_birth, "sex": user_data.sex, "mobile": user_data.mobile, "health_issues": user_data.health_issues}, "medical_store": {"name": clinic.name, "mobile": clinic.mobile, "email": clinic.email, "address": clinic.address, "lat": clinic.lat, "lang": clinic.lang, "lat": clinic.lat, "lang": clinic.lang, "pincode": clinic.pincode, "city": clinic.city, "id": clinic.id, "instore": clinic.instore_pickup,"instore_pickup_radius":clinic.instore_pickup_kms}}
        cart_data.append(data)
    get_carts['data'] = cart_data
    return get_carts

@dunzo_router.get('/getCarts/{cart}')
async def get_carts(cart:int):
    cart = await Cart.get(id=cart)
    dunzo_order = await cart.cartdunzoorders.all()
    if len(dunzo_order) > 0:
        dunzo_order = dunzo_order[0]
    cartsubs = await cart.cartsubmedicines.all()
    user_data = await cart.user
    clinic = await cart.medical_store
    data = {"maindata": cart, "submedicines": cartsubs, "user": {"name": user_data.first_name + " " + user_data.last_name, "id": user_data.id, "age": age(
        user_data.date_of_birth), "dob": user_data.date_of_birth, "sex": user_data.sex, "mobile": user_data.mobile, "health_issues": user_data.health_issues}, "dunzo": dunzo_order, "medical_store": {"name": clinic.name, "mobile": clinic.mobile, "email": clinic.email, "address": clinic.address, "lat": clinic.lat, "lang": clinic.lang, "lat": clinic.lat, "lang": clinic.lang, "pincode": clinic.pincode, "city": clinic.city}}
    return data


@dunzo_router.post('/instoreUpdate')
async def accept_instore(status: OrderStatus, cart: int, background_tasks: BackgroundTasks,expected_delivery: Optional[str] = None):
    cart = await Cart.get(id=cart)
    cart.order_status = status
    if expected_delivery is not None:
        cart.expected_delivery = expected_delivery
    await cart.save()
    user_obj = await cart.user
    medical_store = await cart.medical_store
    background_tasks.add_task(
        notify_users, f"{medical_store.name} has {status} your order", user_obj.notificationIds, cart.id)
    return "cart updated successfully"
    


@dunzo_router.post('/createDunzoTask')
async def create_dunzo_task(status: OrderStatus, cart: int, background_tasks: BackgroundTasks):
    medical_order = await Cart.get(id=cart)
    medical_order.status = status
    user_obj = await cart.user
    if status != "Accepted":
        await medical_order.save()
        background_tasks.add_task(
            notify_users, f"{medical_store.name} has {status} your order", user_obj.notificationIds, cart.id)
    else:
        medical_store = await medical_order.medical_store
        order.medical_store_id = medical_order.medical_store_id
        order.medical_lat = medical_store.lat
        order.medical_lang = medical_store.lang
        await order.save()
        await medical_store.save()
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
        return JsonResponse({"error": "something went wrong please try again"})

    

    



    
    
    
            
        
        
                    




        
                    
            
                

                
        
        
        
    







