from starlette.responses import JSONResponse
# from starlette.requests import Request
from src.apps.base.service_base import BaseService
from .models import *
from typing import TypeVar, Type, Optional
from .pydanticmodels import *


# class CreateUserOrderViewSet(BaseService):
#     model = CreateUserOrder
#     get_schema = GET_CreateUserOrder


# class MedicalAcceptedViewSet(BaseService):
#     model = MedicalAccepted
#     get_schema = GET_MedicalAccepted
class CartViewSet(BaseService):
    model = Cart
    get_schema = GET_Cart


# user_order = CreateUserOrderViewSet()
# medical_accept = MedicalAcceptedViewSet()
cart_view = CartViewSet()
