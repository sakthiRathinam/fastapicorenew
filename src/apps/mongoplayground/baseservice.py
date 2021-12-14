from pydantic import BaseModel, conint
from fastapi_pagination import Params
from typing import TypeVar, Generic, Sequence
import motor.motor_asyncio

collection_type = TypeVar("collection_type",bound=motr.motor_asyncio.AsyncIOMotorCollection)
class MotorCrudService:
    collection: collection_type
    
    async def create(self):
        pass
    