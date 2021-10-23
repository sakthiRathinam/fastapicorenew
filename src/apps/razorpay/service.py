from starlette.responses import JSONResponse
# from starlette.requests import Request
from src.apps.base.service_base import BaseService
from .models import *
from typing import TypeVar, Type, Optional
from .pydanticmodels import *


class RazorPaymentViewSet(BaseService):
    model = RazorPayment
    get_schema = GET_RazorPayment


class MonthlyPlansViewSet(BaseService):
    model = MonthlyPlans
    get_schema = GET_plans


razor_pay = RazorPaymentViewSet()
monthly_pay = MonthlyPlansViewSet()
