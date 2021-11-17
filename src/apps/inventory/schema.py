from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional
from fastapi import UploadFile, File
from datetime import date, datetime, time, timedelta
from src.apps.users.models import Sex
# class Inventory(BaseModel):
#     morning_count: int = 0
#     afternoon_count: int = 0
#     invalid_count: int = 0
#     night_count: int = 0
#     qty_per_time: int = 0
#     total_qty: int = 0
#     command: str = ""
#     is_drug: Optional[bool] = False
#     before_food: Optional[bool] = False
#     is_given: Optional[bool] = False
#     days: int = 0
#     medicine: int
class Medicine(BaseModel):
    name: str
    inventory: int
    price: float
    active: Optional[bool] = False
class NormalMedicine(BaseModel):
    name: str
    clinic: int
    price: float
    active: Optional[bool] = False
class Inventory(BaseModel):
    clinic: int
    title: str
    medicines: Optional[List[Medicine]] = []
    

    
    
