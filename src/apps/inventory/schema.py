from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional
from fastapi import UploadFile, File
from datetime import date, datetime, time, timedelta
from src.apps.users.models import Sex
from enum import Enum, IntEnum

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
    Pending = "Pending"
    Cancelled = "Cancelled"
    DistrubutorCancelled = "DistrubutorCancelled"
    Received = "Received"
    
class AddMedicine(BaseModel):
    name: str
    inventory: int
    price: float
    main_medicine:Optional[int] = None
    active: Optional[bool] = False
class NormalMedicine(BaseModel):
    name: str
    inventory: int
    price: float
    main_medicine:Optional[int] = None
    medicine_type: MedicineTypes
    medicine_verifed : Optional[bool] = False
    active: Optional[bool] = False
class Inventory(BaseModel):
    clinic: int
    title: str
    medicines: Optional[List[AddMedicine]] = []

    
class ClinicMedicine(BaseModel):
    name : str
    clinic : int
    inventory: int
    price: float
    min_qty : float
    medicine_type: MedicineTypes
    subbox_per_boxes: int
    piece_per_subboxes:Optional[int] = 0
    total_boxes: Optional[int] = 0
    total_subboxes: Optional[int] = 0
    total_loose : Optional[int] = 0
    indication_qty: float
    total_qty:  Optional[float] = 0
    is_drug: Optional[bool] = False
    rack: int
    main_medicine: Optional[int] = None


class ClinicRack(BaseModel):
    inventory: int
    clinic: int
    title: str
    medicine: ClinicMedicine
class OrderMedicines(BaseModel):
    name: str
    main_medicine:int
    total_boxes: Optional[int] = 0
    total_subboxes: Optional[int] = 0
    total_loose: Optional[int] = 0
    total_qty:  Optional[float] = 0
    medicine_type: Optional[MedicineTypes] = "Liquid"
    subbox_per_boxes: int
    piece_per_subboxes: Optional[int] = 0
    status: Optional[OrderStatus] = "Pending"


class ClinicOrders(BaseModel):
    details:str
    contact_no:str
    vendor_name:str
    discount:Optional[float] = 0.0
    expected_delivery:date
    amount:float
    advance_paid:Optional[float] = 0.0
    clinic: int
    inventory: int
    status: Optional[OrderStatus] = "Pending"
    orderedMedicines:Optional[List[OrderMedicines]] = None 
class AvailableMedicine(BaseModel):
    medicine: str
    quantity: float
    medicine_type: MedicineTypes
    
class UpdateOrders(BaseModel):
    order: int
    details: str
    contact_no: str
    vendor_name: str
    discount: Optional[float] = 0.0
    expected_delivery: str
    amount: float
    advance_paid: Optional[float] = 0.0
    status: Optional[OrderStatus] = "Pending"

class CheckAvailable(BaseModel):
    medicines: List[AvailableMedicine]
    clinic: int
    
class ChangeRack(BaseModel):
    current_rack:int
    transfer_rack:int
    medicines: Optional[List[ClinicMedicine]] = []

    
    
class RackMin(BaseModel):
    title: str
    id: int    
class ClinicInventory(BaseModel):
    clinic: int
    title: str
    racks:Optional[List[RackMin]] = [] 
    
    
    
    

    

    

    
    
