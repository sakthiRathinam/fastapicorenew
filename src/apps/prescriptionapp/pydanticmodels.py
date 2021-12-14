from src.apps.prescriptionapp.models import *
from tortoise.contrib.pydantic import pydantic_model_creator


#######clinic########
Create_Clinic = pydantic_model_creator(
    Clinic, name="ClinicGet", exclude=("timings", "created", "updated", "id", "clinicTimings", "clinic_images"))
Create_Recopinist = pydantic_model_creator(
    ClinicReceponists, name="createrecoponist", exclude=("id", "created", "updated"))
Create_Doctor = pydantic_model_creator(
    ClinicDoctors, name="ClinicDoctors", exclude=("id", "created", "updated", 'timings'))
Create_Timings = pydantic_model_creator(
    ClinicTimings, name="timings", exclude=("id","created","updated"))
Create_AppointmentSlots = pydantic_model_creator(
    AppointmentSlots, name="AppointmentSlots", exclude=("id", "created", "updated"))
Create_Appointments = pydantic_model_creator(
    Appointments, name="Appointments", exclude=("id", "created", "updated"))
Create_Prescription = pydantic_model_creator(
    Prescription, name="prescription", exclude=("id", "created", "updated"))
Create_PresMedicines = pydantic_model_creator(
    PresMedicines, name="presmedicines", exclude=("id", "created", "updated"))
Create_Medicine = pydantic_model_creator(
    Medicine, name="mainmediciens", exclude=("id", "created", "updated"))
Create_Reports = pydantic_model_creator(
    MedicalReports, name="medicalreports", exclude=("id", "created", "updated"))
Create_PharmacyOwners = pydantic_model_creator(
    PharmacyOwners, name="PharmacyOwners", exclude=("id", "created", "updated"))
Create_LabOwners = pydantic_model_creator(
    LabOwners, name="LabOwners", exclude=("id", "created", "updated"))
Create_ClinicZones = pydantic_model_creator(
    ClinicZones, name="ClinicZones", exclude=("id", "created", "updated", "active"))
Create_LabReports = pydantic_model_creator(
    LabReports, name="labreports", exclude=("id", "created", "updated"))
Create_LabReports = pydantic_model_creator(
    LabReports, name="labreports", exclude=("id", "created", "updated"))
Create_ClinicReports = pydantic_model_creator(
    ClinicReports, name="clinicreports", exclude=("id", "created", "updated", "active"))
Create_IssuePrescription = pydantic_model_creator(
    IssuePrescription, name="issueprescriptions", exclude=("id", "created", "updated"))
Create_Addresses = pydantic_model_creator(
    UserAddress, name="createuseraddressses", exclude=("id", "created", "updated"))
# Create_ClinicVerification = pydantic_model_creator(
#     ClinicVerification, name="clinicverification", exclude=("id", "created", "updated", 'verified'))
GET_Clinic = pydantic_model_creator(
    Clinic, name="ClinicGet")
GET_Recopinist = pydantic_model_creator(
    ClinicReceponists, name="createrecoponist")
GET_Doctor = pydantic_model_creator(
    ClinicDoctors, name="doctors")
GET_Appointments = pydantic_model_creator(
    Appointments, name="appointments")
GET_Appointments = pydantic_model_creator(
    Appointments, name="appointments")
GET_Slots = pydantic_model_creator(
    AppointmentSlots, name="slots")
GET_Prescription = pydantic_model_creator(
    Prescription, name="prescription")
GET_Medicine = pydantic_model_creator(
    Medicine, name="medicines")
GET_PharmacyOwners = pydantic_model_creator(
    PharmacyOwners, name="PharmacyOwners")
GET_PrescriptionTemplates = pydantic_model_creator(
    PrescriptionTemplates, name="prescriptiontemplates")
GET_LabOwners = pydantic_model_creator(
    LabOwners, name="LabOwners")
GET_Reports = pydantic_model_creator(
    MedicalReports, name="MedicalReports")
GET_ClinicZones = pydantic_model_creator(
    ClinicZones, name="ClinicZones")
GET_LabReports = pydantic_model_creator(
    LabReports, name="getlabreports")
GET_SubReports = pydantic_model_creator(
    SubReports, name="getsubreports")
GET_ClinicReports = pydantic_model_creator(
    ClinicReports, name="getclinicreports")
GET_IssuePrescription = pydantic_model_creator(
    IssuePrescription, name="getissueprescriptions")
GET_Addresses = pydantic_model_creator(
    UserAddress, name="useraddresses")

# GET_ClinicVerification = pydantic_model_creator(
#     ClinicVerification, name="ClinicVerification")




