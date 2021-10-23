from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional
from fastapi import UploadFile,File
from datetime import date, datetime, time, timedelta
from .pydanticmodels import Create_PresMedicines, Create_Timings

class AddDoctor(BaseModel):
    clinic: int
    doctor: int
    owner: Optional[bool] = False
    
    
class AddRecopinist(BaseModel):
    clinic: int
    recopinist: int
    start_time : str = ""
    end_time : str = ""
    owner: Optional[bool] = False
    

class Properties(BaseModel):
    language: str = None
    author: str = None
    
class PrescriptionMedicines(BaseModel):
    morning_count : int = 0
    afternoon_count: int = 0
    invalid_count: int = 0
    night_count: int = 0
    qty_per_time: int = 0
    total_qty: int = 0
    command: str = ""
    is_drug: Optional[bool] = False
    before_food: Optional[bool] = False
    is_given: Optional[bool] = False
    days: int = 0
    medicine: int
    
class CreateTemplate(BaseModel):
    diagonsis:str
    command:str
    template:Optional[bool] = False
    medicines_list:List[PrescriptionMedicines]
class AddPrescription(BaseModel):
    active : bool = True
    personal_prescription : bool = False
    contains_drug: Optional[bool] = False
    is_template: Optional[bool] = False
    appointment_taken: Optional[bool] = False
    doctor_fees: int
    user_id : int
    clinic_id : Optional[int] = None
    doctor_id : Optional[int] = None
    receponist_id : Optional[int]
    diagonsis: List[CreateTemplate]
    reports : Optional[List[str]] = []
    

class AddExistingDoctor(BaseModel):
    doctor:int
    clinic:int
    timings: List[Create_Timings]
    owner_access: Optional[bool] = False
    doctor_access: Optional[bool] = False
class CreateClinic(BaseModel):
    name : str
    email: str
    mobile: str
    drug_license: Optional[str] = ""
    gst_no : Optional[str] = ""
    notificationId: Optional[str] = ""
    city: Optional[str] = ""
    state: Optional[str] = ""
    notificationId: Optional[str] = ""
    address: str
    lat: str
    lang: str
    pincode: str
    active: Optional[bool] = True
    
class FilterPharOwners(BaseModel):
    clinic_id:Optional[int] = None
    user_id:Optional[int] = None
    endtime_str: Optional[str] = None
    starttime_str: Optional[str] = None

class SlotDict(BaseModel):
    max_slots:int
    slot_time: str
    
    
class BulkSlot(BaseModel):
    Monday:List[SlotDict]
    Tuesday: List[SlotDict]
    Wednesday: List[SlotDict]
    Thursday: List[SlotDict]
    Friday: List[SlotDict]
    Saturday: List[SlotDict]
    Sunday: List[SlotDict]
    clinic_id: int
    doctor_id: int
