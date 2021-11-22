from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional
from fastapi import UploadFile,File
from datetime import date, datetime, time, timedelta
from .pydanticmodels import Create_PresMedicines, Create_Timings
from .models import AppointmentStatus, MedicineTypes
from src.apps.users.models import User_Pydantic
from src.apps.users.models import Sex
from fastapi import APIRouter, Depends, BackgroundTasks, Response, status, Request, File, UploadFile, Body

class AddDoctor(BaseModel):
    clinic: int
    doctor: int
    owner: Optional[bool] = False
    
class UserMainEdit(BaseModel):
    first_name:Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[str] = None
    address: Optional[str] = None
    sex: Optional[Sex] = None
    qualifications: Optional[List[str]] = None
    health_issues: Optional[List[str]] = None
    specialization: Optional[List[str]] = None
    date_of_birth: Optional[date] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    doctor_fees: Optional[int] = None
class EditUser(BaseModel):
    data: UserMainEdit
    user: int
    
    
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
    morning_count : float = 0
    afternoon_count: float = 0
    invalid_count: float = 0
    night_count: float = 0
    qty_per_time: float = 0
    total_qty: float = 0
    command: str = ""
    medicine_name:str
    medicine_type: MedicineTypes
    is_drug: Optional[bool] = False
    before_food: Optional[bool] = False
    is_given: Optional[bool] = False
    days: int = 0
    medicine_id: int


class PatientCreation(BaseModel):
    username: str
    mobile: str
    first_name: str
    password: str
    sex: str
    health_issues: Optional[List[str]] = []
    last_name: Optional[str] = None
    is_child: Optional[bool] = False
    date_of_birth: date

class EditClinicReport(BaseModel):
    price:int
    active:Optional[bool] = True
    
class CreateClinicReports(BaseModel):
    clinic_id: int
    general_report_id: int
    price: int
    title: str
class CreateTemplate(BaseModel):
    diagonsis:str
    command:str
    template:Optional[bool] = False
    pres_medicines:List[PrescriptionMedicines]
    medicines_given:List[PrescriptionMedicines]
class AddPrescription(BaseModel):
    active : bool = True
    next_visit: Optional[date] = None
    personal_prescription : bool = False
    contains_drug: Optional[bool] = False
    is_template: Optional[bool] = False
    appointment_taken: Optional[bool] = False
    doctor_fees: int
    user_id : Optional[int] = None
    user_create: Optional[PatientCreation] = None
    clinic_id : Optional[int] = None
    doctor_id : Optional[int] = None
    receponist_id : Optional[int] = None
    medicines: List[CreateTemplate]
    reports : Optional[List[str]] = []
    appointment: Optional[int] = None
    reason: Optional[str] = None
    

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
    max_slots:Optional[int] = 0
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
    
class CreateSubReport(BaseModel):
    report: str
    expected_result: Optional[datetime] = datetime.now()
class CreateLabReport(BaseModel):
    active :Optional[bool] = True
    user_id:int
    clinic_id:int
    expected_result:Optional[datetime] = datetime.now()
    sub_reports:List[CreateSubReport]
    
    
class AppointmentCreation(BaseModel):
    user_id:Optional[int] = None
    user_create:Optional[PatientCreation] = None
    requested_date: Optional[date]
    accepted_date: Optional[date]
    status: Optional[AppointmentStatus] = AppointmentStatus.Pending
    accepted_slot_id : Optional[int]
    requested_slot_id: Optional[int]
    doctor_id:Optional[int]
    clinic_id:int
    reason:str
class EditAppointment(BaseModel):
    user_id:Optional[int] = None
    requested_date: Optional[date] = None
    accepted_date: Optional[date] = None
    status: Optional[AppointmentStatus] = AppointmentStatus.Pending
    accepted_slot_id : Optional[int] = None
    requested_slot_id: Optional[int] = None
    doctor_id:Optional[int] = None
    reason:Optional[str] = None
    
