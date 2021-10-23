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


class OrderStatus(str, Enum):
    Accepted = "Accepted"
    Declined = "Declined"
    Pending = "Pending"
    Delivered = "Delivered"

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
    medicinesordered: fields.ReverseRelation["CreateUserOrder"]
    
    
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
    
class MedicalAccepted(models.Model):
    order: fields.ForeignKeyRelation[Clinic] = fields.ForeignKeyField(
        "models.CreateUserOrder", related_name="medicalstoresaccepted", null=True, blank=True)
    status: MedicalAcceptStatus = fields.CharEnumField(
        MedicalAcceptStatus, default=MedicalAcceptStatus.WAITING)
    accepted_price = fields.FloatField(default=0)
    medical_store: fields.ForeignKeyRelation[Clinic] = fields.ForeignKeyField(
        "models.Clinic", related_name="medicalacceptedorders", null=True, blank=True)
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    all_available = fields.BooleanField(default=False)
    

    

class DunzoOrder(models.Model):
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    to_send = fields.JSONField(null=True)
    current_response = fields.JSONField(null=True)
    task_id = fields.CharField(max_length=300,null=True)
    refund_id = fields.CharField(max_length=500,null=True)
    medical_store: fields.ForeignKeyRelation[Clinic] = fields.ForeignKeyField(
        "models.Clinic", related_name="medicaldunzoorders", null=True, blank=True)
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
    main_order: fields.ForeignKeyRelation[CreateUserOrder] = fields.ForeignKeyField(
        "models.CreateUserOrder", related_name="createuserorders", null=True, blank=True)



    
    
    
    
    
    
    
     
    

    

    
    
    

    
