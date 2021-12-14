from tortoise import fields, models, Tortoise, run_async
from tortoise.contrib.pydantic import pydantic_model_creator
from enum import Enum, IntEnum
from typing import List
from tortoise.exceptions import NoValuesFetched
from tortoise.models import Model
from tortoise.signals import post_delete, post_save, pre_delete, pre_save
from src.apps.users.models import User
from src.apps.base.additionalfields import StringArrayField
from src.apps.prescriptionapp.models import Clinic, PresMedicines, Prescription , Medicine


class DunzoState(str, Enum):
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"
    ACTIVE = "ACTIVE"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
    PENDING = "PENDING"
    

class OrderState(str, Enum):
    Instore = "Instore"
    Dunzo = "Dunzo"
    UserPickup = "UserPickup"
    
# class MedicalAcceptStatus(str, Enum):
#     WAITING = "WAITING"
#     REJECTED = "REJECTED"
#     DELIVERED = "DELIVERED"
#     ACCEPTED = "DELIVERED"
#     CANCELLED = "CANCELLED"
#     PENDING = "PENDING"
    
class DunzoPayments(str, Enum):
    COD = "COD"
    DUNZO_CREDIT = "DUNZO_CREDIT"
    
class PaymentStatus(str, Enum):
    Pending = "Pending"
    Success = "Success"
    Failed = "Failed"

class MedicalAcceptStatus(str, Enum):
    WAITING = "WAITING"
    REJECTED = "REJECTED"
    DELIVEREDTODUNZO = "DELIVEREDTODUNZO"
    ACCEPTED = "ACCEPTED"
    CANCELLED = "CANCELLED"
    USERCANCELLED = "USERCANCELLED"
    DUNZOCANCELLED = "DUNZOCANCELLED"
    DUNZODELIVERED = "DUNZODELIVERED"
    REQUESTED = "REQUESTED"

class OrderType(str, Enum):
    Offline = "Offline"
    Zomato = "Zomato"
    Dunzo = "Dunzo"
    Instore = "Instore"
    Swiggy = "Swiggy"


class MedicineTypes(str, Enum):
    Liquid = "Liquid"
    Tablet = "Tablet"
    Capsules = "Capsules"
    Cream = "Cream"
    Powder = "Powder"
    Lotion = "Lotion"
    Soap = "Soap"
    Shampoo = "Shampoo"
    Suspension = "Suspension"
    Serum = "Serum"
    Oil = "Oil"
    Inhalers = "Inhalers"
    Injections = "Injections"
    Suppositories = "Suppositories"
    Solution = "Solution"
    Others = "Others" 
    
class OrderStatus(str, Enum):
    Accepted = "Accepted"
    Declined = "Declined"
    Pending = "Pending"
    Delivered = "Delivered"
    TimeOutCancelled = "TimeOutCancelled"
    PaymentWaiting = "PaymentWaiting"

class OrderMedicines(models.Model):
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    medicine: fields.ForeignKeyRelation[Medicine] = fields.ForeignKeyField(
        "models.Medicine", related_name="dunzoorderedmedicines", null=True, blank=True)
    medicine_time: fields.ForeignKeyRelation[PresMedicines] = fields.ForeignKeyField(
        "models.PresMedicines", related_name="dunzopresmedicines", null=True, blank=True)
    quantity = fields.IntField(default=0)
    price = fields.FloatField(default=0)
    changed_price = fields.FloatField(default=0)
    is_drug = fields.BooleanField(default=False)
    
    
class CreateUserOrder(models.Model):
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    clinic: fields.ManyToManyRelation["Clinic"] = fields.ManyToManyField(
        "models.Clinic", related_name="clinicorders"
    )
    ordered_medicines: fields.ManyToManyRelation["OrderMedicines"] = fields.ManyToManyField(
        "models.OrderMedicines", related_name="medicinesordered", through="event_teams"
    )
    order_status: DunzoState = fields.CharEnumField(
        DunzoState, default=DunzoState.PENDING)
    order_mode: OrderType = fields.CharEnumField(
        OrderType, default=OrderType.Dunzo)
    medical_store: fields.ForeignKeyRelation[Clinic] = fields.ForeignKeyField(
        "models.Clinic", related_name="useracceptedorders", null=True, blank=True)
    prescription: fields.ForeignKeyRelation[Prescription] = fields.ForeignKeyField(
        "models.Prescription", related_name="prescriptionorders", null=True, blank=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="usercreatedorders")
    user_lat = fields.CharField(max_length=600, null=True, blank=True)
    user_lang = fields.CharField(max_length=600, null=True, blank=True)
    medical_lat = fields.CharField(max_length=600, null=True, blank=True)
    medical_lang = fields.CharField(max_length=600, null=True, blank=True)
    total_price = fields.FloatField(default=0)
    discount_price = fields.IntField(default=0)
    accepted_price = fields.IntField(default=0)
    

    
class Cart(models.Model):
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    medical_store: fields.ForeignKeyRelation[Clinic] = fields.ForeignKeyField(
        "models.Clinic", related_name="medicalstorecarts", null=True, blank=True)
    is_received = fields.BooleanField(default=False)
    lat = fields.FloatField(default=0)
    lang = fields.FloatField(default=0)
    order_status: OrderStatus = fields.CharEnumField(
        OrderStatus, default=OrderStatus.Pending)
    order_mode: OrderState = fields.CharEnumField(
        OrderState, default=OrderState.Dunzo)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="userdunzocarts")
    prescription: fields.ForeignKeyRelation[Prescription] = fields.ForeignKeyField(
        "models.Prescription", related_name="cartprescriptions", null=True, blank=True)
    total_price = fields.IntField(default=0)
    expected_delivery = fields.CharField(max_length=500,null=True,blank=True)
    address = fields.TextField(null=True,blank=True,nax_length=4000)
    pincode = fields.CharField(max_length=20,null=True,blank=True)
    landmark = fields.CharField(max_length=1100,null=True,blank=True)
    

class CartSubs(models.Model):
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    received = fields.BooleanField(default=False)
    medicine_name = fields.CharField(max_length=1200, null=True, blank=True)
    medicine_type: MedicineTypes = fields.CharEnumField(
        MedicineTypes, default=MedicineTypes.Capsules)
    quantity = fields.IntField(default=0)
    price = fields.IntField(default=0)
    cart: fields.ForeignKeyRelation[Cart] = fields.ForeignKeyField(
        "models.Cart", related_name="cartsubmedicines")
    medicine: fields.ForeignKeyRelation[Medicine] = fields.ForeignKeyField(
    "models.Medicine", related_name="cartsubmedicines")





class DunzoOrder(models.Model):
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    to_send = fields.JSONField(null=True)
    current_response = fields.JSONField(null=True)
    cart: fields.ForeignKeyRelation[Cart] = fields.ForeignKeyField(
        "models.Cart", related_name="cartdunzoorders")
    task_id = fields.CharField(max_length=300,null=True)
    refund_id = fields.CharField(max_length=500,null=True)
    medical_store: fields.ForeignKeyRelation[Clinic] = fields.ForeignKeyField(
        "models.Clinic", related_name="medicalstoredunzoorders", null=True, blank=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="userdunzoorders")
    task_id = fields.CharField(max_length=500, null=True, blank=True)
    order_id = fields.CharField(max_length=300, null=True, blank=True)
    payment_id = fields.CharField(max_length=300, null=True, blank=True)
    is_refunded = fields.BooleanField(default=False)
    is_delivered = fields.BooleanField(default=False)
    current_state = fields.CharField(max_length=500, null=True, blank=True)
    is_cancelled = fields.BooleanField(default=False)
    refund_id = fields.CharField(max_length=400, null=True, blank=True)
    estimated_price = fields.FloatField(null=True)
    razor_price = fields.FloatField(null=True)
    razor_commision = fields.IntField(null=True, blank=True)
    is_received = fields.BooleanField(default=False)  # payment received
    amount = fields.IntField(default=0)
    payment_status: PaymentStatus = fields.CharEnumField(
        PaymentStatus, default=PaymentStatus.Pending)
    dunzo_status: DunzoState = fields.CharEnumField(
        DunzoState, default=DunzoState.PENDING)
    payment_method: DunzoPayments = fields.CharEnumField(
        DunzoPayments, default=DunzoPayments.DUNZO_CREDIT)
    

    



    




    
    
    
    
    
    
    
     
    

    

    
    
    

    
