from src.apps.auth.security import get_password_hash, verify_password
from src.apps.auth.security import verify_password, get_password_hash
import uuid
from starlette.responses import JSONResponse
# from starlette.requests import Request
from src.apps.users.models import User
from starlette import status
from .models import *
from src.config.settings import BASE_DIR, STATIC_ROOT, MEDIA_ROOT
from src.apps.users.views import get_current_login, get_session_current_login
from src.apps.base.service_base import CustomPage
from fastapi import APIRouter, Depends, BackgroundTasks, Response, status, Request, File, UploadFile, Body, HTTPException
from tortoise.query_utils import Q
import pathlib
from typing import List , Optional
from src.apps.users.models import User, User_Pydantic
from src.apps.users.service import user_service
import os
import shutil
from .service import *
from .schema import *
from .pydanticmodels import *
from fastapi_pagination import LimitOffsetPage, Page, add_pagination
from fastapi_pagination.ext.tortoise import paginate
import datetime
clinto_router = APIRouter(dependencies=[Depends(get_session_current_login)])
days = ["Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"]
@clinto_router.get('/doctorClinics/{userid}')
async def getClinics(userid: int):
    user = await User.get(id=userid).prefetch_related("workingclinics")
    clinics = [{"name": clinic.name, "email": clinic.email}async for clinic in user.workingclinics.all()]

@clinto_router.post('/createClinic')
async def createClinic(clinic: Create_Clinic = Body(...),zone_id:Optional[int]=Body(...)):
    if zone_id is None:
        clinic_obj = await Clinic.create(**clinic.dict(exclude_unset=True))
    else:
        clinic_obj = await Clinic.create(**clinic.dict(exclude_unset=True),zone_id=zone_id)
    # path = pathlib.Path(
    #     MEDIA_ROOT, f"clinicmainimages/{str(clinic_obj.id)+file.filename}")
    # os.makedirs(os.path.dirname(path), exist_ok=True)
    # with path.open('wb') as write:
    #     shutil.copyfileobj(file.file, write)
    # clinic_obj.display_picture = path
    # await clinic_obj.save()
    # print(file.filename)
    # print(create_clinic)
    return clinic_obj
    
@clinto_router.get('/getClinics')
async def get_clinics(limit: int = 10, offset: int = 0, type: Optional[Types] = Types.Clinic,id:Optional[int]=None):
    if id is not None:
        clinic = await Clinic.get(id=id)
        timings = await clinic.timings.all().values('timings', 'day')
        return {"clinic_data": clinic, "timings": timings}
    clinics = await clinic_view.limited_data(limit=limit, offset=offset, types=type)
    clinics_objs = []
    for clinic in clinics['data']:
        timings = await clinic.timings.all().values('timings','day')
        clinics_objs.append({"clinic_data": clinic, "timings": timings})
    return {**clinics, "data": clinics_objs}

@clinto_router.put('/editClinic')
async def edit_clinic(clinic:int,data:Create_Clinic = Body(...)):
    updated_clinic = await Clinic.filter(id=clinic).update(**data.dict(exclude_unset=True))
    return {"clinic updated successfully"}


@clinto_router.put('/updateDp')
async def edit_display_profile(user:int,dp:Optional[UploadFile]= File(...)):
    user_obj = await User.get(id=user)
    sample_uuid = uuid.uuid4()
    path = pathlib.Path(
        MEDIA_ROOT, f"clinicimages/{str(sample_uuid)+dp.filename}")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with path.open('wb') as write:
        shutil.copyfileobj(dp.file, write)
    user_obj.display_picture = path
    await user_obj.save()
    return "display picture updated successfully"


@clinto_router.put('/changePassword')
async def edit_password(newpassword: str = Body(...), user:int=Body(...),oldpassword:str=Body(...)):
    user_obj = await User.get(id=user)
    if verify_password(oldpassword,user_obj.password):
        hashed_password = get_password_hash(newpassword)
        user_obj.password = hashed_password
        await user_obj.save()
        return "password changed successfully"
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Wrong Old Password"
    )

@clinto_router.put('/editUser')
async def edit_user(data: EditUser):
    data_dict = data.data.dict()
    user_dict = {k: v for k, v in data_dict.items() if v is not None}
    qualifications = None
    health_issues = None
    specialization = None
    if 'qualifications' in user_dict:
        qualifications = user_dict.pop('qualifications')
    if 'health_issues' in user_dict:
        health_issues = user_dict.pop('health_issues')
    if 'specialization' in user_dict:
        specialization = user_dict.pop('specialization')
    user_update = await User.filter(id=data.user).update(**user_dict)
    user_obj = await User.get(id=data.user)
    if qualifications is not None:
        print(type(qualifications),"awfawef")
        user_obj.qualifications = qualifications
    if health_issues is not None:
        user_obj.health_issues = health_issues
    if specialization is not None:
        print(type(specialization),"awef")
        user_obj.specialization = specialization
    await user_obj.save()
    return user_obj
    
@clinto_router.delete('/deleteClinic/{clinic}')
async def edit_clinic(clinic:int):
    updated_clinic = await Clinic.get(id=clinic).delete()
    return {"clinic delete successfully"}
@clinto_router.put('/editClinic')
async def edit_clinic(clinic:int,data:Create_Clinic = Body(...)):
    updated_clinic = await Clinic.filter(id=clinic).update(**data.dict(exclude_unset=True))
    return {"clinic updated successfully"}

@clinto_router.post('/addDoctors')
async def add_doctors(data: Create_Doctor, user: User_Pydantic,clinic: int = Body(...)):
    if await User.filter(Q(username=user.username) | Q(email=user.email)).exists():
        user = await User.filter(Q(username=user.username) | Q(email=user.email)).first()
    else:
        user = await user_service.create_user(user)
    create_doctor = await ClinicDoctors.create(clinic_id=clinic, user_id=user, **data.dict(exclude_unset=True))
    return create_doctor

@clinto_router.post('/addRecoponist')
async def add_doctors(data: Create_Recopinist, user: User_Pydantic, clinic: int = Body(...)):
    if await User.filter(Q(username=user.username) | Q(email=user.email)).exists():
        user = await User.filter(Q(username=user.username) | Q(email=user.email)).first()
        user_id = user.id
    else:
        user = await user_service.create_user(user)
        user_id = user.id
    create_recopinist = await ClinicReceponists.create(clinic_id=clinic, user_id=user_id, **data.dict(exclude_unset=True))
    return create_recopinist

@clinto_router.post("/addClinicImages")
async def clinic_images(clinic: int,files: List[UploadFile] = File(...)):
    file_paths = []
    clinic_obj = await Clinic.get(id=clinic)
    for file in files:
        sample_uuid = uuid.uuid4()
        path = pathlib.Path(
        MEDIA_ROOT, f"clinicimages/{str(sample_uuid)+file.filename}")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        file_paths.append(str(path))
        with path.open('wb') as write:
            shutil.copyfileobj(file.file, write)
    if clinic_obj.clinic_images is not None:
        clinic_obj.clinic_images.extend(file_paths)
    clinic_obj.clinic_images = file_paths
    await clinic_obj.save()
    return clinic_obj

@clinto_router.post("/addTimings")
async def add_timings(timings: List[Create_Timings],clinic: bool=Body(...), clinicid: int=Body(...)):
    if clinic:
        for time in timings:
            clinic_timings = await Clinic.get(id=clinicid).prefetch_related('timings')
            timings_obj = await clinic_timings.timings.filter(day=time.day).first()
            timings_obj.timings = time.timings
            await timings_obj.save()
    if not clinic:
        for time in timings:
            timings_obj =await ClinicTimings.get(doctor_id=clinicid,day=time.day)
            timings_obj.timings = time.timings
            await timings_obj.save()
    return {"success":"timing updated"}

@clinto_router.get("/getDoctorClinics")
async def get_doctor_clinics(doctor:int):
    doctor_obj = await User.get(id=doctor).prefetch_related("workingclinics")
    working_clinics = await doctor_obj.workingclinics.all().prefetch_related("clinic")
    clinics_list = []
    for clinics in working_clinics:
        clinic = await clinics.clinic
        clinics_list.append({"clinic":clinic,"details":clinics})
    return {"working_clinics": clinics_list,"user":doctor_obj}

@clinto_router.get("/getLabOwnerClinics")
async def get_lab_clinics(owner:int):
    owner_obj = await User.get(id=owner).prefetch_related("labownerusers")
    working_clinics = await owner_obj.labownerusers.all().prefetch_related("clinic")
    clinics_list = []
    for clinics in working_clinics:
        clinic = await clinics.clinic
        clinics_list.append({"clinic":clinic,"details":clinics})
    return {"working_clinics": clinics_list,"user":owner_obj}

@clinto_router.get("/getPharOwnerClinics")
async def get_phar_owners_clinics(owner:int):
    owner_obj = await User.get(id=owner).prefetch_related("pharmacyownersusers")
    working_clinics = await owner_obj.pharmacyownersusers.all().prefetch_related("clinic")
    clinics_list = []
    for clinics in working_clinics:
        clinic = await clinics.clinic
        clinics_list.append({"clinic":clinic,"details":clinics})
    return {"working_clinics": clinics_list,"user":owner_obj}

@clinto_router.get("/getRecopClinics")
async def get_recop_clinics(recop:int):
    doctor_obj = await User.get(id=recop).prefetch_related("workingshops")
    working_clinics = await doctor_obj.workingshops.all().prefetch_related("clinic")
    clinics_list = []
    for clinics in working_clinics:
        clinic = await clinics.clinic
        clinics_list.append({"clinic":clinic,"details":clinics})
    return {"working_clinics": clinics_list,"user":doctor_obj}

# @clinto_router.post('/addRecopinist')
# async def add_recopinist(data: Create_Recopinist):
#     create_recopinist = await ClinicReceponists.create(clinic_id=clinic, user_id=user, **data.dict(exclude_unset=True))
#     return create_recopinist

@clinto_router.post('/addSlot')
async def add_slots(data: Create_AppointmentSlots,clinicid: int = Body(...),doctor:int = Body(...)):
    create_slot = await AppointmentSlots.create(clinic_id=clinicid, doctor_id=doctor, **data.dict(exclude_unset=True))
    return create_slot

# @clinto_router.post('/addAppointments')
# async def add_appointments(data: Create_Appointments, clinicid: int = Body(...), user: int = Body(...), slot: int = Body(...), accepted_slot: Optional[int] = Body(...)):
#     print(data)
#     if accepted_slot is None:
#         create_appointment = await Appointments.create(clinic_id=clinicid,user_id=user,requested_slot_id=slot,**data.dict(exclude_unset=True))
#     if accepted_slot is not None:
#         create_appointment = await Appointments.create(clinic_id=clinicid, user_id=user, requested_slot_id=slot,accepted_slot_id=accepted_slot **data.dict(exclude_unset=True))
#     return create_appointment
@clinto_router.post('/addAppointments')
async def add_appointments(data: AppointmentCreation):
    if data.user_create is not None:
        user = await User.create(**data.user_create.dict())
        data.user_id = user.id
    create_appointment = await Appointments.create(**data.dict(exclude_unset=True))
    return create_appointment

@clinto_router.put('/editAppointments/{id}')
async def add_appointments(data: EditAppointment,id:int):
    edit_appointment = await appointment_view.update(data,id=id)
    return edit_appointment




@clinto_router.get('/getAppointments')
async def get_appointments(limit: int, offset: int, request:Request,clinic:Optional[int] = None,status: Optional[AppointmentStatus]=None,date:Optional[str]=None,doctor:Optional[int]= None,user:Optional[int]=None):
    params_dict = {**request.query_params}
    print(params_dict)
    filter_dict = dict()
    if clinic is not None:
        filter_dict['clinic_id'] = clinic
    if date is not None:
        filter_dict["requested_date"] = date
    if doctor is not None:
        filter_dict["doctor_id"] = doctor
    if user is not None:
        filter_dict["user_id"] = user
    if status is not None:
        filter_dict['status'] = status
    toReturn =await appointment_view.limited_data(limit=limit,offset=offset,**filter_dict)
    data_list = []
    for data in toReturn['data']:
        clinic_obj = await data.clinic
        user_obj = await data.user
        doctor_obj = await data.doctor
        requested_slot = await data.requested_slot
        accepted_slot = await data.accepted_slot
        extra = {"clinic": {"name": clinic_obj.name, "id": clinic_obj.id, "mobile": clinic_obj.mobile, "lat": clinic_obj.lat, "lang": clinic_obj.lang}, "user": {"name": user_obj.first_name + " " + user_obj.last_name, "id": user_obj.id, "age": age(user_obj.date_of_birth),"dob":user_obj.date_of_birth, "sex": user_obj.sex, "mobile": user_obj.mobile,"health_issues":user_obj.health_issues}, "doctor": {
            "name": doctor_obj.first_name + " " + doctor_obj.last_name, "id": doctor_obj.id, "age": age(doctor_obj.date_of_birth), "sex": doctor_obj.sex}, "slot": {"requested": requested_slot.slot_time, "accepted": accepted_slot.slot_time if accepted_slot is not None else None}}
        extra_data = {"appointment":data,"extra":extra}
        data_list.append(extra_data)
    return {**toReturn,"data":data_list}
weekday_dict = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday',
    5: 'Friday', 6: 'Saturday', 0: 'Sunday'}
@clinto_router.get('/getSlots')
async def get_appointmentslots(limit: int, offset: int,clinic:int, day: Optional[Days]=None, doctor: Optional[int] = None,weekday:Optional[int]=None):
    if weekday is not None:
        day = weekday_dict[weekday]
    if doctor is None:
        if day is not None:
            toReturn = await slot_view.limited_data(limit=limit, offset=offset, clinic_id=clinic,day=day)
        else:
            toReturn = await slot_view.limited_data(limit=limit, offset=offset, clinic_id=clinic)

        data_list = []
        for data in toReturn['data']:
            doctor = await data.doctor
            doctor = {"id":doctor.id,"name":doctor.first_name + " " + doctor.last_name}
            data_obj = {"slot": data, 'doctor_extra': doctor}
            data_list.append(data_obj)
        return {**toReturn,"data":data_list}
    if day is None:
        toReturn = await slot_view.limited_data(
        limit=limit, offset=offset, doctor_id=doctor,clinic_id=clinic)
    else:
        toReturn = await slot_view.limited_data(limit=limit, offset=offset, clinic_id=clinic,day=day,doctor_id=doctor) 
        
    data_list = []
    for data in toReturn['data']:
        doctor = await data.doctor
        doctor = {"id": doctor.id,
                  "name": doctor.first_name + " " + doctor.last_name}
        data_obj = {"slot": data, 'doctor_extra': doctor}
        data_list.append(data_obj)
    return {**toReturn, "data": data_list}
@clinto_router.delete('/deleteSlots/{item_id}')
async def delete_slots(item_id: int):
    await slot_view.delete(id=item_id)
    return {"success":"delteed successfully"}


@clinto_router.put('/editSlot')
async def add_slots(data: Create_AppointmentSlots,id:int,doctor: Optional[int] = None):
    if doctor is  None:
        create_slot = await slot_view.update_extra(id, schema)(id,data)
    create_slot = await slot_view.update_extra(id, data,doctor_id=doctor)
    return create_slot

days = ["Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"]
@clinto_router.post('/bulkSlot')
async def add_slots(data: BulkSlot):
    data_dict = data.dict()
    slot_objs = []
    for day in days:
        current_day = data_dict[day]
        slots = [AppointmentSlots(
            **data, clinic_id=data_dict['clinic_id'],doctor_id=data_dict['doctor_id'],day=day) for data in current_day]
        slot_objs.extend(slots)
    creation = await AppointmentSlots.bulk_create(slot_objs)
    return creation



@clinto_router.post('/addPrescription')
async def add_prescription(data:AddPrescription):
    pres_obj = Prescription()
    if data.personal_prescription:
        if data.doctor is None:
            raise HTTPException(
                status_code=status.HTTP_500_BAD_REQUEST, detail="Doctor is mandatory"
            )
        else:
            doctor_obj = await User.get(id=data.doctor_id)
            if data.user_id is not None:
                user_obj = await User.get(id=data.user_id)
            if data.user_create is not None:
                user_dict = data.user_create.dict()
                hashed_password = get_password_hash(
                    user_dict.pop('password'))
                user_obj = await User.create(**user_dict, password=hashed_password)
            pres_obj = await Prescription.create(clinic=clinic_obj, doctor=doctor_obj, user=user_obj, doctor_fees=data.doctor_fees, next_visit=data.next_visit,personal=True,age=age(user_obj.date_of_birth))
            for diag in data.medicines:
                diag_obj, created = await Diagonsis.get_or_create(title=diag.diagonsis)
                if diag.template:
                    pres_template = await PrescriptionTemplates.create(diagonsis=diag_obj, personal=False, doctor_obj=doctor_obj, command=diag.command)
                for medicine in diag.pres_medicines:
                    medicine_obj = await PresMedicines.create(**medicine.dict(exclude_unset=True), diagonsis=diag_obj, diagonsisName=diag_obj.title)
                    await pres_obj.medicines.add(medicine_obj)
                    if medicine_obj.is_drug:
                        pres_obj.contains_drug = True
                    if diag.template:
                        await pres_template.medicines.add(medicine_obj)
                for medicine in diag.medicines_given:
                    medicine_obj = await PresMedicines.create(**medicine.dict(exclude_unset=True), diagonsis=diag_obj, diagonsisName=diag_obj.title)
                    await pres_obj.medicines.add(medicine_obj)
                    if diag.template:
                        await pres_template.medicines.add(medicine_obj)
                await pres_obj.diagonsis_list.add(diag_obj)
            for report in data.reports:
                report_obj = await MedicalReports.get_or_create(title=report)
                await pres_obj.reports.add(report_obj)
            await pres_obj.save()
    else:
        if data.clinic_id is None and data.doctor_id is None:
            raise HTTPException(
                status_code=status.HTTP_500_BAD_REQUEST, detail="Clinic is mandatory"
            )
        else:
            clinic_obj = await Clinic.get(id=data.clinic_id)
            doctor_obj = await User.get(id=data.doctor_id)
            print(data)
            if data.user_id is not None:
                user_obj = await User.get(id=data.user_id)
                print("imhereeeasddd")
            if data.user_create is not None:
                print("awgefasdddd")
                user_dict = data.user_create.dict()
                hashed_password = get_password_hash(
                    user_dict.pop('password'))
                user_obj = await User.create(**user_dict, password=hashed_password)
            pres_obj = await Prescription.create(clinic=clinic_obj, doctor=doctor_obj, user=user_obj, doctor_fees=data.doctor_fees, next_visit=data.next_visit, reason=data.reason,age=age(user_obj.date_of_birth),blood_sugar=data.blood_sugar,blood_pressure=data.blood_pressure,weight=data.weight)
            for diag in data.medicines:
                diag_obj,created = await Diagonsis.get_or_create(title=diag.diagonsis)
                if diag.template:
                    pres_template = await PrescriptionTemplates.create(diagonsis=diag_obj, personal=False, doctor_obj=doctor_obj, command=diag.command)
                for medicine in diag.pres_medicines:
                    print(medicine,"imhereee")
                    medicine_obj = await PresMedicines.create(**medicine.dict(exclude_unset=True),diagonsis=diag_obj,diagonsisName=diag_obj.title)
                    await pres_obj.medicines.add(medicine_obj)
                    if medicine_obj.is_drug:
                        pres_obj.contains_drug = True
                    if diag.template:
                        await pres_template.medicines.add(medicine_obj)
                for medicine in diag.medicines_given:
                    medicine_obj = await PresMedicines.create(**medicine.dict(exclude_unset=True), diagonsis=diag_obj, diagonsisName=diag_obj.title)
                    await pres_obj.medicines.add(medicine_obj)
                    if diag.template:
                        await pres_template.medicines.add(medicine_obj)
                await pres_obj.diagonsis_list.add(diag_obj)
            if data.invalid_till is not None:
                pres_obj.invalid_till = data.invalid_till
                pres_obj.contains_drug = True
            for report in data.reports:
                report_obj,created = await MedicalReports.get_or_create(title=report)
                await pres_obj.medical_reports.add(report_obj)
            await pres_obj.save()
            if data.appointment is not None:
                appointment_obj = await Appointments.get(id=data.appointment)
                appointment_obj.status = "Completed"
                await appointment_obj.save()
                return JSONResponse({"success":"prescription created successfully and appoinment updated successfully","pres_obj":pres_obj.id},status_code=201) 
            return JSONResponse({"success":"prescription created successfully","pres_obj":pres_obj.id},status_code=201)
        
        
@clinto_router.get('/getReportPrescription')
async def get_pres_reports(pres:int):
    pres_obj = await Prescription.get(id=pres)
    reports = []
    for report in await pres_obj.medical_reports.all():
        reports.append({"title":report.title,"id":report.id})
    return reports
@clinto_router.get('/getPrescriptions')
async def get_prescriptions(clinic:Optional[int]=None,doctor:Optional[int]=None,user:Optional[int]=None,limit:int=10,offset:int=0,created:datetime.date=None):
    if user is None:
        if clinic is not None:
            pres_objs = await prescription_view.limited_data(limit=limit, offset=offset, clinic_id=clinic,created__istartswith=str(created))
        if doctor is not None:
            pres_objs = await prescription_view.limited_data(limit=limit, offset=offset, doctor_id=doctor,created__istartswith=str(created))
    else:
        pres_objs = await prescription_view.limited_data(limit=limit, offset=offset, user_id=user,active=True)
    to_send = []
    for pres in pres_objs['data']:
        clinic = None
        receponist = None
        doctor = None
        user = await pres.user
        if pres.clinic_id is not None:
            clinic = await pres.clinic
        if pres.doctor_id is not None:
            doctor = await pres.doctor
        if pres.receponist is not None:
            receponist = await pres.receponist
        pres_full = {"main_data": pres, "medicines_given": await pres.medicines.filter(is_given=True).only('morning_count', 'afternoon_count', 'invalid_count', 'night_count', 'qty_per_time','diagonsisName', 'total_qty', 'command', 'medicine_name', 'is_drug', 'before_food', 'is_given', 'days', 'medicine_id', 'medicine_type'), "pres_medicines": await pres.medicines.filter(is_given=False).only('morning_count', 'afternoon_count', 'invalid_count', 'night_count', 'qty_per_time', 'total_qty', 'diagonsisName','command', 'medicine_name', 'is_drug', 'before_food', 'is_given', 'days', 'medicine_id', 'medicine_type'),"clinic":{"name":clinic.name,"mobile":clinic.mobile,"email":clinic.email,"address":clinic.address,"lat":clinic.lat,"lang":clinic.lang,"lat":clinic.lat,"lang":clinic.lang,"pincode":clinic.pincode,"city":clinic.city} if clinic is not None else None,"user":{"name":user.first_name + " "+user.last_name,"mobile":user.mobile,"id":user.id,"age":age(user.date_of_birth),"sex":user.sex,"health_issues":user.health_issues,"dob":user.date_of_birth},"doctor":{"name":doctor.first_name + " "+doctor.last_name,"id":doctor.id,"mobile":doctor.mobile,"email":doctor.email,"specialization":doctor.specialization} if doctor is not None else None,"diagonsis_list":[diag.title async for diag in  pres.diagonsis_list],"created_by":doctor.first_name + " " + doctor.last_name if receponist is None else recponist.first_name + " " + recoponist.last_name,"suggested_reports":[report.title for report in await pres.medical_reports.all()]}
        to_send.append(pres_full)
    pres_objs['data'] = to_send
    return pres_objs
@clinto_router.get('/getPrescriptions/{id}')
async def get_single_prescriptions(id:int):
        pres = await Prescription.get(id=id)
        clinic = None
        receponist = None
        doctor = None
        user = await pres.user
        if pres.clinic_id is not None:
            clinic = await pres.clinic
        if pres.doctor_id is not None:
            doctor = await pres.doctor
        if pres.receponist is not None:
            receponist = await pres.receponist
        pres_full = {"main_data": pres, "medicines_given": await pres.medicines.filter(is_given=True).only('morning_count', 'afternoon_count', 'invalid_count', 'night_count', 'qty_per_time','diagonsisName', 'total_qty', 'command', 'medicine_name', 'is_drug', 'before_food', 'is_given', 'days', 'medicine_id', 'medicine_type'), "pres_medicines": await pres.medicines.filter(is_given=False).only('morning_count', 'afternoon_count', 'invalid_count', 'night_count', 'qty_per_time', 'total_qty', 'diagonsisName','command', 'medicine_name', 'is_drug', 'before_food', 'is_given', 'days', 'medicine_id', 'medicine_type'),"clinic":{"name":clinic.name,"mobile":clinic.mobile,"email":clinic.email,"address":clinic.address,"lat":clinic.lat,"lang":clinic.lang,"lat":clinic.lat,"lang":clinic.lang,"pincode":clinic.pincode,"city":clinic.city} if clinic is not None else None,"user":{"name":user.first_name + " "+user.last_name,"mobile":user.mobile,"id":user.id,"age":age(user.date_of_birth),"sex":user.sex,"health_issues":user.health_issues,"dob":user.date_of_birth},"doctor":{"name":doctor.first_name + " "+doctor.last_name,"id":doctor.id,"mobile":doctor.mobile,"email":doctor.email,"specialization":doctor.specialization} if doctor is not None else None,"diagonsis_list":[diag.title async for diag in  pres.diagonsis_list],"created_by":doctor.first_name + " " + doctor.last_name if receponist is None else recponist.first_name + " " + recoponist.last_name,"suggested_reports":[report.title for report in await pres.medical_reports.all()]}
        return pres_full
@clinto_router.get('/searchPrescriptions')
async def search_prescriptions(search:Optional[int]=None):
    pres_objs = await Prescription.filter(
        Q(user__mobile=str(search)) | Q(id=search)).filter(invalid_till__gt=datetime.date.today())
    to_send = []
    for pres in pres_objs:
        clinic = None
        receponist = None
        doctor = None
        user = await pres.user
        if pres.clinic_id is not None:
            clinic = await pres.clinic
        if pres.doctor_id is not None:
            doctor = await pres.doctor
        if pres.receponist is not None:
            receponist = await pres.receponist
        pres_full = {"main_data": pres, "medicines_given": await pres.medicines.filter(is_given=True).only('morning_count', 'afternoon_count', 'invalid_count', 'night_count', 'qty_per_time','diagonsisName', 'total_qty', 'command', 'medicine_name', 'is_drug', 'before_food', 'is_given', 'days', 'medicine_id', 'medicine_type'), "pres_medicines": await pres.medicines.filter(is_given=False).only('morning_count', 'afternoon_count', 'invalid_count', 'night_count', 'qty_per_time', 'total_qty', 'diagonsisName','command', 'medicine_name', 'is_drug', 'before_food', 'is_given', 'days', 'medicine_id', 'medicine_type'),"clinic":{"name":clinic.name,"mobile":clinic.mobile,"email":clinic.email,"address":clinic.address,"lat":clinic.lat,"lang":clinic.lang,"lat":clinic.lat,"lang":clinic.lang,"pincode":clinic.pincode,"city":clinic.city} if clinic is not None else None,"user":{"name":user.first_name + " "+user.last_name,"mobile":user.mobile,"id":user.id,"age":age(user.date_of_birth),"sex":user.sex,"health_issues":user.health_issues,"dob":user.date_of_birth},"doctor":{"name":doctor.first_name + " "+doctor.last_name,"id":doctor.id,"mobile":doctor.mobile,"email":doctor.email,"specialization":doctor.specialization} if doctor is not None else None,"diagonsis_list":[diag.title async for diag in  pres.diagonsis_list],"created_by":doctor.first_name + " " + doctor.last_name if receponist is None else recponist.first_name + " " + recoponist.last_name,"suggested_reports":[report.title for report in await pres.medical_reports.all()]}
        to_send.append(pres_full)
    return to_send
@clinto_router.get('/searchDiagonsis')
async def search_diagonsis(name:str,doctor:int):
    diagonsis_objs = await Diagonsis.filter(title__istartswith=name).only('title','active','id')
    if len(diagonsis_objs) > 5:
        diagonsis_objs = diagonsis_objs[:5]
    diag_objs = []
    for diag in diagonsis_objs:
        doctor_templates = await PrescriptionTemplates.filter(doctor_obj_id=doctor,diagonsis=diag).prefetch_related('medicines')
        diag_full = {"diag": diag, "template": [{"details": template, "medicines_given": await template.medicines.filter(is_given=True).only('morning_count', 'afternoon_count', 'invalid_count', 'night_count', 'qty_per_time', 'total_qty', 'command', 'medicine_name', 'is_drug', 'before_food', 'is_given', 'days', 'medicine_id','medicine_type'), "pres_medicines": await template.medicines.filter(is_given=False).only('morning_count', 'afternoon_count', 'invalid_count', 'night_count', 'qty_per_time', 'total_qty', 'command', 'medicine_name', 'is_drug', 'before_food', 'is_given', 'days', 'medicine_id','medicine_type')} for template in doctor_templates]}
        diag_objs.append(diag_full)
    return diag_objs



        


@clinto_router.post('/addExistingDoctor')
async def add_prescription(data: AddExistingDoctor):
    clinic_doctor,created = await ClinicDoctors.get_or_create(user_id=data.doctor,clinic_id=data.clinic,owner_access=data.owner_access,doctor_access=data.doctor_access)
    for time in data.timings:
        timings_obj = await clinic_doctor.timings.filter(day=time.day)
        timings_obj = timings_obj[0]
        if timings_obj is not None:
            timings_obj.timings = time.timings
            await timings_obj.save()
        else:
            print("not found")
    return {"success":"doctor added success"}

@clinto_router.post('/invalidPrescription')
async def invalid_prescription(prescription:int= Body(...),invalid:bool= Body(...)):
    pres_obj = await Prescription.get(id=prescription)
    pres_obj.active = False
    await pres_obj.save()
    return "prescription invalid status changed successfully"

@clinto_router.get('/getFullDetail')
async def clinic_full_detail(clinic_id:int):
    clinic_obj = await Clinic.get(id=clinic_id).prefetch_related('workingreceponists','doctors')
    working_doctors =await clinic_obj.doctors.all().prefetch_related('user','timings')
    doctors = []
    for doctor in working_doctors:
        timings = [{"day":doctortiming.day,"timings":doctortiming.timings} for doctortiming in await doctor.timings.all().only('day','timings')]
        user = await doctor.user
        basic_detials = {"dp": user.display_picture, "name": user.first_name +
                         user.last_name, "id": doctor.id, "userid":user.id,"email": user.email}
        doctors.append({"details":basic_detials,"timings":timings})
    recopinists =await clinic_obj.workingreceponists.all().prefetch_related('user')
    recoponists_array = []
    for recop in recopinists:
        user = await recop.user
        basic_detials = {"dp": user.display_picture, "name": user.first_name +
                         user.last_name, "id": recop.id, "email": user.email, "startime": recop.starttime_str, "userid": user.id, "endtime": recop.endtime_str}
        recoponists_array.append(basic_detials)
    return {"doctors": doctors, "recoponists": recoponists_array}

clinto_router.redirect_slashes = False

@clinto_router.delete('/clinicWorkers')
async def delete_clinic_members(worker:int,doctor:Optional[bool]=False):
    if doctor:
        s = await ClinicDoctors.get(id=worker).delete()
        if s:
            return {"success":"doctor deleted"}
        else:
            return {"failed":"doctor does not exist"}
    s = await ClinicReceponists.get(id=worker).delete()
    if s:
        return {"success": "recoponist deleted"}
    else:
        return {"failed": "recoponist does not exist"}
    



def age(date) -> int:
    if date is not None:
        year = 365.2425
        start_date = date
        end_date = datetime.date.today()
        age = round((end_date - start_date).days // year)
        return age
    return 0

@clinto_router.get('/doctorList')
async def get_doctors():
    doctors = await User.filter(roles="Doctor")
    doctors_detail = []
    for doctor in doctors:
        doctor_profile = {"name": doctor.first_name + doctor.last_name, "age": age(doctor.date_of_birth), "qualification": doctor.qualifications,
                          "specialization": doctor.specialization, "email": doctor.email, "address": doctor.address, "state": doctor.state, "city": doctor.city,"working_clinics":[]}
        working_clinics = await doctor.workingclinics.all()
        for clinic in working_clinics:
            clinic_obj = await clinic.clinic
            doctor_profile['working_clinics'].append({"clinicname": clinic_obj.name, "city": clinic_obj.city, "state": clinic_obj.state,
                                                      "address": clinic_obj.address, "pincode": clinic_obj.pincode, "display_picture": clinic_obj.display_picture, "lat": clinic_obj.lat, "lang": clinic_obj.lang})
        doctors_detail.append(doctor_profile)
    return doctors_detail

@clinto_router.delete('/deleteClinicImages')
async def delete_image(index:int,clinic:int):
    clinic_obj = await Clinic.get(id=clinic)
    image_path = clinic_obj.clinic_images.pop(index)
    media_path = os.remove(image_path)
    await clinic_obj.save()
    return {"success":"image deleted"}
            
@clinto_router.post('/addMedicines')
async def add_medicines(data: Create_Medicine = Body(...)):
    add_medicine = await medicine_view.create(data)
    return {"medicine":"medicine created successfully","medicine_obj":add_medicine}

@clinto_router.delete('/deleteMedicines')
async def delete_medicines(id:int):
    await medicine_view.delete(id=id)
    return {"success":"deleted"}

@clinto_router.put('/updateMedicines')
async def update_medicines(id:int,data:Create_Medicine= Body(...)):
    await medicine_view.update(data,id=id)
    return {"success":"updated"}

@clinto_router.get('/filtermedicines')
async def filter_medicines(request: Request, title: Optional[str] = None, type: Optional[MedicineTypes] = None):
    query_params = request.query_params
    if type is not None:
        medicines = await Medicine.filter(**query_params,title__istartswith=title)
    else:
        print("im heree")
        medicines = await Medicine.filter(title__istartswith=title)
        return medicines

@clinto_router.post('/addPharamacyOwners')
async def add_medicines(data: Create_PharmacyOwners = Body(...),clinic:int=Body(...),user:int=Body(...)):
    add_medicine = await PharmacyOwners.create(**data.dict(exclude_unset=True),user_id=user,clinic_id=clinic)
    return {"success":"created successfully"}

@clinto_router.delete('/deletePharOwners')
async def delete_pharowners(id:int):
    await pharmacy_owner_view.delete(id=id)
    return {"success":"deleted"}

@clinto_router.put('/updatePharOwners')
async def update_pharowners(id:int,data:Create_PharmacyOwners= Body(...)):
    await pharmacy_owner_view.update(data, id=id)
    return {"success":"updated"}

@clinto_router.get('/filterPharOwners')
async def filterPharOwners(clinic_id:Optional[int]=None,user_id:Optional[int]=None):
    if clinic_id is not None:
        owners = await PharmacyOwners.filter(clinic_id=clinic_id).prefetch_related('user')
    owner_list = []
    for owner in owners:
        user = await owner.user
        user_obj = {"name":user.first_name + " "+user.last_name,"mobile":user.mobile,"dp":user.display_picture}
        owner_list.append({"owner":owner,"userdetail":user_obj})
    return {"data": owner_list}

@clinto_router.get('/getPharOwners')
async def get_phar_owners(limit:int=10,offset:int=0):
    owners = await pharmacy_owner_view.limited_data(limit=limit, offset=offset)
    owner_list = []
    for owner in owners['data']:
        user = await owner.user
        user_obj = {"name": user.first_name + " "+user.last_name,
                    "mobile": user.mobile, "dp": user.display_picture}
        owner_list.append({"owner": owner, "userdetail": user_obj})
    return {**owners,"data":owner_list}
@clinto_router.get('/getLabOwners')
async def get_lab_owners(limit:int=10,offset:int=0):
    owners = await lab_owner_view.limited_data(limit=limit, offset=offset)
    owner_list = []
    for owner in owners['data']:
        user = await owner.user
        user_obj = {"name": user.first_name + " "+user.last_name,
                    "mobile": user.mobile, "dp": user.display_picture}
        owner_list.append({"owner": owner, "userdetail": user_obj})
    return {**owners, "data": owner_list}
@clinto_router.post('/addLabOwners')
async def add_medicines(data: Create_LabOwners = Body(...),clinic: int = Body(...), user: int = Body(...)):
    add_medicine = await LabOwners.create(**data.dict(exclude_unset=True), user_id=user, clinic_id=clinic)
    return {"success": "created successfully"}

@clinto_router.delete('/deleteLabOwners')
async def delete_medicines(id:int):
    await lab_owner_view.get(id=id).delete()
    return {"success":"deleted"}

@clinto_router.put('/updateLabOwners')
async def update_medicines(id: int, data: Create_LabOwners = Body(...)):
    await lab_owner_view.update(data, id=id)
    return {"success":"updated"}


@clinto_router.get('/filterlabOwners')
async def filter_lab_owners(clinic_id: Optional[int] = None, user_id: Optional[int] = None):
    if clinic_id is not None:
        owners = await LabOwners.filter(clinic_id=clinic_id).prefetch_related('user')
    owner_list = []
    for owner in owners:
        user = await owner.user
        user_obj = {"name": user.first_name + " "+user.last_name,
                    "mobile": user.mobile, "dp": user.display_picture}
        owner_list.append({"owner": owner, "userdetail": user_obj})
    return  owner_list

@clinto_router.get('/mainMedicines')
async def main_medicines(limit:int=10,offset:int=0,active:bool=True,search:bool=False):
    next_items = False
    previous_items = False
    total_items = await Medicine.filter(active=active).count()
    medicines = await Medicine.filter(active=active)
    if not search:
        if offset > 0:
            previous_items = True
        if total_items < (offset/limit) * limit:
            next_items = True
    return medicines

@clinto_router.post('/addReports')
async def add_medicines(data: Create_Reports = Body(...)):
    add_medicine = await report_view.create(data)
    return {"medicine":"medicine created successfully","medicine_obj":add_medicine}

@clinto_router.post('/addClinicReports')
async def add_clinic_report(data: CreateClinicReports = Body(...)):
    add_medicine = await ClinicReports.create(**data.dict())
    return {"success":"clinic report added successfully"}

@clinto_router.get('/getClinicReports')
async def get_clinic_reports(limit: int = 10, offset:int = 0,title:Optional[str]=None,active:Optional[bool]=True,clinic:Optional[int]=None):
    search_dict = dict()
    search_dict['active'] = active
    if title is not None:
        search_dict['title__istartswith'] = title
    if clinic is not None:
        search_dict['clinic_id'] = clinic
    reports = await clinic_reports.limited_data(limit=limit, offset=offset, **search_dict)
    return reports


@clinto_router.put('/editClinicReports')
async def edit_clinic_report(id:int=Body(...),price:int=Body(...),active:Optional[bool] = True):
    clinic_report_obj = await ClinicReports.get(id=id)
    if price is not None:
        clinic_report_obj.price = price
    clinic_report_obj.active = active
    await clinic_report_obj.save()
    return "clinic report added successfully"
    # clinic_report_obj


@clinto_router.delete('/deleteClinicReports')
async def delete_clinic_reports(id:int):
    await ClinicReports.filter(id=id).delete()
    return "clinic report deleted successfully"
    


@clinto_router.post('/addLabReports')
async def add_medicines(data: CreateLabReport):
    report_obj = data.dict()
    sub_reports = report_obj.pop('sub_reports')
    if data.user_id is  None:
        user_dict = report_obj.pop('user_create')
        hashed_password = get_password_hash(
            user_dict.pop('password'))
        user_obj = await User.create(**user_dict, password=hashed_password)
        report_obj['user_id'] = user_obj.id
    lab_report = await LabReports.create(**report_obj)
    total = 0
    for report in sub_reports:
        report_obj = await ClinicReports.get(id=report['report'])
        sub_report = await SubReports.create(report_id=report_obj.id, expected_result=report['expected_result'], report_name=report_obj.title,price=report_obj.price)
        total += report_obj.price
        await lab_report.sub_reports.add(sub_report)
    lab_report.total_price = total
    await lab_report.save()
    return {"success": "report created successfully", "report_obj": lab_report}

@clinto_router.delete('/deleteReports')
async def delete_medicines(id:int):
    await report_view.delete(id=id)
    return {"success":"deleted"}

@clinto_router.put('/updateReports')
async def update_medicines(id: int, data: Create_Reports = Body(...)):
    await report_view.update(data, id=id)
    return {"success":"updated"}

@clinto_router.get('/filterReports')
async def filter_medicines(data: GET_Reports = Body(...)):
    reports = await report_view.filter(**data.dict(exclude_unset=True))
    return reports


@clinto_router.get('/getReports')
async def get_reports(limit: int = 10, offset:int = 0,title:Optional[str]=None,active:Optional[bool]=True):
    search_dict = dict()
    search_dict['active'] = active
    if title is not None:
        search_dict['title__istartswith'] = title
    reports = await report_view.limited_data(limit=limit, offset=offset, **search_dict)
    return reports

@clinto_router.get('/getClinicReports')
async def get_reports(clinic:int,limit: int = 10, offset:int = 0,title:Optional[str]=None,active:Optional[bool]=True):
    search_dict = dict()
    search_dict['active'] = active
    search_dict['clinic_id'] = clinic
    if title is not None:
        search_dict['title__istartswith'] = title
    reports = await clinic_reports.limited_data(limit=limit, offset=offset, **search_dict)
    return reports


@clinto_router.post('/editSubReports')
async def edit_sub_reports(subreport:int,file:Optional[UploadFile] = File(...)):
    sub_report = await SubReports.get(id=subreport)
    sample_uuid = uuid.uuid4()
    path = pathlib.Path(
        MEDIA_ROOT, f"reportimages/{str(sample_uuid)+file.filename}")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with path.open('wb') as write:
        shutil.copyfileobj(file.file, write)
    sub_report.file = path
    sub_report.status = 'Completed'
    await sub_report.save()
    
@clinto_router.put('/removeSubReport')
async def edit_sub_reports(subreport:int=Body(...),labreport:int=Body(...)):
    sub_report = await SubReports.get(id=subreport)
    lab_report = await LabReports.get(id=labreport)
    await lab_report.sub_reports.remove(sub_report)
    await lab_report.save()
    return "sub report removed successfully"


@clinto_router.delete('/deleteLabReport')
async def edit_sub_reports(labreport: int):
    await LabReports.filter(id=labreport).delete()
    return "lab report deleted successfully"
    
@clinto_router.get('/getLabReports')
async def get_reports(limit: int = 10, offset:int = 0,clinic:Optional[int]=None,active:Optional[bool]=True,date:Optional[datetime.date] = None):
    search_dict = dict()
    search_dict['active'] = active
    if clinic is not None:
        search_dict['clinic_id'] = clinic
    if date is not None:
        search_dict['created__istartswith'] = str(date)
    reports = await lab_reports.limited_data(limit=limit, offset=offset, **search_dict)
    report_data = []
    for report in reports['data']:
        if report.clinic_id is not None:
            clinic = await report.clinic
        if report.user_id is not None:
            user = await report.user
        data = {
            "main_data":report,"clinic":{"name":clinic.name,"mobile":clinic.mobile,"email":clinic.email,"address":clinic.address,"lat":clinic.lat,"lang":clinic.lang,"lat":clinic.lat,"lang":clinic.lang,"pincode":clinic.pincode,"city":clinic.city} if clinic is not None else None,"user":{"name":user.first_name + " "+user.last_name,"mobile":user.mobile,"id":user.id,"age":age(user.date_of_birth),"sex":user.sex,"health_issues":user.health_issues,"dob":user.date_of_birth} if user is not None else None,"subreports":[{"file":subreport.file,"expected_result":subreport.expected_result,"id":subreport.id,"report":subreport.report_name,"price":subreport.price}for subreport in await report.sub_reports.all()]
        }
        report_data.append(data)
    reports['data'] = report_data
    return reports

@clinto_router.get('/getLabReports/{id}/')
async def get_single_reports(id:int):
    report = await LabReports.get(id=id)
    if report.clinic_id is not None:
        clinic = await report.clinic
    if report.user_id is not None:
        user = await report.user
    data = {
        "main_data":report,"clinic":{"name":clinic.name,"mobile":clinic.mobile,"email":clinic.email,"address":clinic.address,"lat":clinic.lat,"lang":clinic.lang,"lat":clinic.lat,"lang":clinic.lang,"pincode":clinic.pincode,"city":clinic.city} if clinic is not None else None,"user":{"name":user.first_name + " "+user.last_name,"mobile":user.mobile,"id":user.id,"age":age(user.date_of_birth),"sex":user.sex,"health_issues":user.health_issues,"dob":user.date_of_birth} if user is not None else None,"subreports":[{"file":subreport.file,"expected_result":subreport.expected_result,"id":subreport.id,"report":subreport.report_name,"price":subreport.price}for subreport in await report.sub_reports.all()]
    }
    return data

@clinto_router.post('/createZones')
async def add_medicines(data: Create_ClinicZones = Body(...)):
    create_obj = await clinic_zones.create(data)
    return {"success":"created successfully"}


@clinto_router.delete('/deleteZones')
async def delete_medicines(id:int):
    await clinic_zones.delete(id=1)
    return {"success":"deleted"}

@clinto_router.put('/updateZones')
async def update_medicines(id: int, data: Create_ClinicZones = Body(...)):
    await clinic_zones.update(data, id=id)
    return {"success":"updated"}

@clinto_router.get('/filterZones')
async def filter_medicines(name:str):
    zones = await ClinicZones.filter(title__istartswith=name)
    return zones

@clinto_router.get('/getZones')
async def get_zones(limit: int=10,offset:int=0):
    zones = await clinic_zones.limited_data(limit=limit,offset=offset)
    return zones

@clinto_router.get('/paginateMedicines', response_model=CustomPage[GET_Medicine])
async def paginate_mediciens(request: Request) -> any:
    medicines = await paginate(Medicine.all())
    extra = {'previous':False,"next":True}
    if request.query_params['page'] != str(1):
        extra['previous'] = True
    if (int(request.query_params['page']) * int(request.query_params['size']))+1 > medicines.total:
        extra['next'] = False
    data = {**medicines.dict(),**extra}
    return medicines


@clinto_router.post('/issuePrescription')
async def issue_prescription(data: IssuePres):
    # pres_obj = await Prescription.get(id=data.prescription_id)
    # if pres_obj.invalid_till is not None:
    #     if datetime.date.today() > pres_obj.invalid_till:
    #         raise HTTPException(
    #             status_code=status.HTTP_500_BAD_REQUEST, detail="Prescriptions is invalid canmot issue this prescription"
    #         )    
    pres_obj = await IssuePrescription.create(**data.dict())
    return "prescription issued succcessfully"
@clinto_router.get('/getIssuePrescription')
async def get_issue_prescription(date:datetime.date,clinic:int,limit:Optional[int]=10,offset:Optional[int]=0):
    issue_objs = await issue_prescription_view.limited_data(limit=limit, offset=offset, clinic_id=clinic, created__istartswith=str(date))
    to_send = []
    for issue in issue_objs['data']:
        user = await issue.user
        user_obj = {"name": user.first_name + " "+user.last_name,
                    "mobile": user.mobile, "dp": user.display_picture,"age":age(user.date_of_birth),"sex":user.sex}
        to_send.append({"main":issue,"user_detail":user_obj})
    issue_objs['data'] = to_send
    return issue_objs

# @clinto_router.get('/issuePrescription')
# async def issue_prescription(data: IssuePres):
#     pres_obj = await IssuePrescription.create(**data.dict())
#     return "prescription issued succcessfully"














# @clinto_router.post('/addMedicines')
# async def add_medicines(data: Create_Medicine = Body(...)):
#     add_medicine = await medicine_view.create(data)
#     return {"medicine":"medicine created successfully","medicine_obj":add_medicine}

# @clinto_router.delete('/deleteMedicines')
# async def delete_medicines(id:int):
#     await medicine_view.delete(id=1)
#     return {"success":"deleted"}

# @clinto_router.put('/updateMedicines')
# async def update_medicines(id:int,data:Create_Medicine= Body(...)):
#     await medicine_view.update(data,id=id)
#     return {"success":"updated"}

# @clinto_router.put('/filtermedicines')
# async def filter_medicines(data: GET_Medicine = Body(...)):
#     await medicine_view.filter(**data.dict(exclude_unset=True))
#     return {"success":"updated"}
        


    
    
    
    
    
    
    
    




    
        
        
    
    


        













    









    
    

