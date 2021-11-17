
from starlette.responses import JSONResponse
# from starlette.requests import Request
from src.apps.base.service_base import BaseService
from .models import *
from typing import TypeVar, Type, Optional
from .pydanticmodels import *
ModelType = TypeVar("ModelType", bound=models.Model)

###############################################viewsets###########################################
class ClincViewSet(BaseService):
    model = Clinic
    get_schema = GET_Clinic
    
class ReceponistViewSet(BaseService):
    model = ClinicReceponists
    get_schema = GET_Recopinist

class DoctorViewSet(BaseService):
    model = ClinicReceponists
    get_schema = GET_Doctor
    
class MedicineViewSet(BaseService):
    model = Medicine
    get_schema = GET_Doctor
    
class PrescriptionViewSet(BaseService):
    model = Prescription
    get_schema = GET_Prescription
    
class PrescriptionMedicines(BaseService):
    model = PresMedicines
    get_schema = GET_Prescription
    
    
class AppointmentViewSet(BaseService):
    model = Appointments
    get_schema = GET_Appointments
    

class SlotViewSet(BaseService):
    model = AppointmentSlots
    get_schema = GET_Slots
    
class MedicineViewSet(BaseService):
    model = Medicine
    get_schema = GET_Medicine
    
    
class ReportViewSet(BaseService):
    model = MedicalReports
    get_schema = GET_Reports


class PharmacyOwnersViewSet(BaseService):
    model = PharmacyOwners
    get_schema = GET_PharmacyOwners
class LabOwnersViewSet(BaseService):
    model = LabOwners
    get_schema = GET_LabOwners
class ClinicZonesViewSet(BaseService):
    model = ClinicZones
    get_schema = GET_ClinicZones
    
##########################################routers#####################################################
clinic_view = ClincViewSet()
receponist_view = ReceponistViewSet()
doctor_view = DoctorViewSet()
appointment_view = AppointmentViewSet()
slot_view = SlotViewSet()
prescription_view = PrescriptionViewSet()
medicine_view = MedicineViewSet()
report_view = ReportViewSet()
lab_owner_view = LabOwnersViewSet()
pharmacy_owner_view = PharmacyOwnersViewSet()
clinic_zones = ClinicZonesViewSet()
# clinic_verify = ClinicVerifyViewSet()



    
    
    




