from tortoise import fields, models, Tortoise, run_async
from tortoise.contrib.pydantic import pydantic_model_creator
from enum import Enum, IntEnum
from typing import List
import datetime
from tortoise.exceptions import NoValuesFetched
from tortoise.signals import post_delete, post_save, pre_delete, pre_save

from src.apps.base.additionalfields import StringArrayField
from src.apps.prescriptionapp.models import Clinic
from src.apps.users.models import User


class RazorPayPlans(str, Enum):
    Monthly = "Monthly"
    Quarterly = "Quarterly"
    Yearly = "Yearly"
    Halfly = "Halfly"


class RazorPayStatus(str, Enum):
    Pending = "Pending"
    Success = "Success"
    Failed = "Failed"
    Refunded = "Refunded"


class PaymentModes(str, Enum):
    upi = "upi"
    cash = "cash"
    card = "card"


class RazorPayment(models.Model):
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    subscription: RazorPayPlans = fields.CharEnumField(
        RazorPayPlans, default=RazorPayPlans.Monthly)
    status: RazorPayStatus = fields.CharEnumField(
        RazorPayStatus, default=RazorPayStatus.Pending)
    payment_mode: PaymentModes = fields.CharEnumField(
        PaymentModes, default=PaymentModes.upi)
    order_id = fields.CharField(max_length=800, null=True, blank=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="userpayments")
    clinic: fields.ForeignKeyRelation[Clinic] = fields.ForeignKeyField(
        "models.Clinic", related_name="clinicpayments")
    is_received = fields.BooleanField(default=False)
    is_refunded = fields.BooleanField(default=False)
    amount = fields.IntField(default=0)
    subscription_date = fields.DateField(null=True, blank=True)
    valid_till = fields.DateField(null=True, blank=True)
    is_cash = fields.BooleanField(default=False)
    active = fields.BooleanField(default=True)


class MonthlyPlans(models.Model):
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    main_subscription: RazorPayPlans = fields.CharEnumField(
        RazorPayPlans, default=RazorPayPlans.Monthly)
    amount = fields.IntField(default=0)
    discount = fields.IntField(default=0)
    discount_percent = fields.FloatField(default=0)
