from typing import Optional

from tortoise.query_utils import Q

from src.apps.auth.security import verify_password, get_password_hash
from typing import TypeVar, Type, Optional
from . import schema
from .models import *
from ..base.service_base import BaseService




class UserService(BaseService):
    model = User
    create_schema = User_Pydantic
    update_schema = User_Pydantic
    get_schema = UserIn_Pydantic
    query_schema = UserIn_Pydantic

    async def create_user(self,user:User_Pydantic,**kwargs):
        hashed_password = get_password_hash(user.dict().pop('password'))
        return await self.create(self.create_schema(**user.dict(exclude={'password'}),password=hashed_password,**kwargs))
    async def authenticate(self,username:str,password:str) -> Optional[User]:
        user = await self.model.get(username=username)
        if not user:
            return None
        if not verify_password(password,user.password):
            return None
        return user
    async def change_password(self,user:User,password:str):
        hashed_password = get_password_hash(password)
        user.password = hashed_password
        user.save()
    async def search_user(self,search:str,**kwargs):
        return await self.model.get_or_none(Q(username=search) | Q(email=search))
    async def change_active(self,active:bool,search:str,**kwargs) ->Optional[str]:
        user =await self.model.get_or_none(username=search)
        if user is not None:
            if active:
                user.is_active = True
                user.save()
                return "activated"
            if not active:
                user.is_active = False
                user.save()
                return "deactivated"
        return "usernotexists"
    async def create_superuser(self,user:User_Pydantic,**kwargs):
        hashed_password = get_password_hash(user.dict().pop('password'))
        return await self.create(self.create_schema(**user.dict(exclude={'password'}),password=hashed_password,is_superuser=True,**kwargs))

    
class ClinicVerifyViewSet(BaseService):
    model = ClinicVerification
    get_schema = Create_ClinicVerification


user_service = UserService()
clinic_verify = ClinicVerifyViewSet()
