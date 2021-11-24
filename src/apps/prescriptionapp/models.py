from tortoise import fields, models, Tortoise, run_async
from tortoise.contrib.pydantic import pydantic_model_creator
from enum import Enum, IntEnum
from typing import List
from tortoise.exceptions import NoValuesFetched
from tortoise.models import Model
from tortoise.signals import post_delete, post_save, pre_delete, pre_save
from src.apps.users.models import User ,Inventory
from src.apps.base.additionalfields import StringArrayField
class Types(str, Enum):
    MedicalStore = "MedicalStore"
    Clinic = "Clinic"
    Others = "Others"
    Lab = "Lab"
    
    
class SubTypes(str, Enum):
    eye = "eye"
    dental = "dental"
    cardiology = "cardiology"
    dermatology = "dermatology"
    throat = "throat"
    nose = "nose"
    normal = "normal"
    gastroenterology = "gastroenterology"
    obstetrics = "obstetrics"
    podiatry = "podiatry"
    neurology = "neurology"
    physicaltherapy = "physicaltherapy"
    urology = "urology"
    ophthalmology = "ophthalmology"
    oncology = "oncology"
    orthopedics = "orthopedics"
    homeo = "homeo"
    vetnary = "vetnary"
    
class InventoryCategory(str, Enum):
    Doctor = "Doctor"
    MedicalStore = "MedicalStore"
    Clinic = "Clinic"
    Lab = "Lab"
    
class AppointmentStatus(str, Enum):
    Requested = "Requested"
    Accepted = "Accepted"
    Cancelled = "Cancelled"
    Completed = "Completed"
    ClinicCancelled = "ClinicCancelled"
    Pending = "Pending"
    
class Days(str,Enum):
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"
    Sunday = "Sunday"
    
class SlotDays(str,Enum):
    All = "All"
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"
    Sunday = "Sunday"
    
    
class MedicineTypes(str,Enum):
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
    
# class Inventory(models.Model):
#     created = fields.DatetimeField(auto_now_add=True)
#     updated = fields.DatetimeField(auto_now=True)
#     title = fields.CharField(max_length=400)
#     types: InventoryCategory = fields.CharEnumField(
#         InventoryCategory, default=InventoryCategory.Clinic)

class ClinicTimings(models.Model):
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    day: Days = fields.CharEnumField(Days, default=Days.Monday)
    timings = StringArrayField()
    clinictimigs: fields.ReverseRelation["Clinic"]
    doctortimings: fields.ReverseRelation["ClinicDoctors"]

class ClinicZones(models.Model):
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    title = fields.CharField(max_length=1000,unique=True)
    active = fields.BooleanField(default=True)

class Clinic(models.Model):
    name = fields.CharField(max_length=400, index=True)
    email = fields.CharField(max_length=600,null=True,blank=True)
    mobile = fields.CharField(max_length=20,null=True,blank=True)
    drug_license = fields.CharField(max_length=1000,null=True,blank=True)
    notificationId = fields.CharField(max_length=500, null=True, blank=True)
    address = fields.TextField(max_length=5000,null=True,blank=True)
    types: Types = fields.CharEnumField(Types,default=Types.Clinic)
    sub_types: SubTypes = fields.CharEnumField(SubTypes,default=SubTypes.eye,null=True,blank=True)
    total_ratings = fields.IntField(default=0)
    city = fields.CharField(null=True, max_length=500, blank=True)
    state = fields.CharField(null=True, max_length=500, blank=True)
    lat = fields.CharField(null=True, max_length=500)
    lang = fields.CharField(null=True, max_length=500)
    zone: fields.ForeignKeyRelation[ClinicZones] = fields.ForeignKeyField(
        "models.ClinicZones", related_name="clinicavailable", null=True, blank=True)
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    display_picture = fields.CharField(null=True, max_length=2000,blank=True)
    pincode = fields.CharField(null=True, max_length=300,blank=True)
    gst_percentage = fields.FloatField(default=0)
    discount_percent = fields.IntField(default=0)
    gst_no = fields.CharField(max_length=1000, null=True, blank=True)
    clinic_images = StringArrayField(null=True)
    created_subs = fields.BooleanField(default=False)
    inventoryIncluded = fields.BooleanField(default=False)
    timings: fields.ManyToManyRelation["ClinicTimings"] = fields.ManyToManyField(
        "models.ClinicTimings", related_name="clinictimigs")
    inventory: fields.ForeignKeyRelation[Inventory] = fields.ForeignKeyField(
        "models.Inventory", related_name="clinicinventories",null=True, blank=True)
    active = fields.BooleanField(default=True)
    # def clinicTimings(self) -> str:
    #     if self.timings.all() is not None:
    #         return [timing.timings for timing in self.timings.all()]
    #     return "opened"

    class PydanticMeta:
        computed = []
        exclude = ('timings',
                   'clinic_images')





    
class ClinicDoctors(models.Model):
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="workingclinics")
    clinic: fields.ForeignKeyRelation[Clinic] = fields.ForeignKeyField(
        "models.Clinic", related_name="doctors")
    timings: fields.ManyToManyRelation["ClinicTimings"] = fields.ManyToManyField(
        "models.ClinicTimings", related_name="doctortimigs", through="doctor_timings"
    )
    personal_inventory = fields.BooleanField(default=False)
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    active = fields.BooleanField(default=False)
    owner_access = fields.BooleanField(default=False)
    doctor_access = fields.BooleanField(default=True)
    subs = fields.BooleanField(default=False)
    
    
class PharmacyOwners(models.Model):
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="pharmacyownersusers")
    clinic: fields.ForeignKeyRelation[Clinic] = fields.ForeignKeyField(
        "models.Clinic", related_name="pharmacyownersusers")
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    starttime_str = fields.CharField(max_length=600, null=True, blank=True)
    endtime_str = fields.CharField(max_length=600, null=True, blank=True)
class LabOwners(models.Model):
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="labownerusers")
    clinic: fields.ForeignKeyRelation[Clinic] = fields.ForeignKeyField(
        "models.Clinic", related_name="labownersusers")
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    starttime_str = fields.CharField(max_length=600, null=True, blank=True)
    endtime_str = fields.CharField(max_length=600, null=True, blank=True)
class ClinicReceponists(models.Model):
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    starttime_str = fields.CharField(max_length=600, null=True, blank=True)
    endtime_str = fields.CharField(max_length=600, null=True, blank=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="workingshops")
    clinic: fields.ForeignKeyRelation[Clinic] = fields.ForeignKeyField(
        "models.Clinic", related_name="workingreceponists")
    types: InventoryCategory = fields.CharEnumField(
        InventoryCategory, default=InventoryCategory.Clinic)
    
class AppointmentSlots(models.Model):
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    slot_time = fields.CharField(max_length=900,null=True,blank=True)
    date = fields.DateField(null=True, blank=True)
    clinic: fields.ForeignKeyRelation[Clinic] = fields.ForeignKeyField(
        "models.Clinic", related_name="clinicslots")
    max_slots = fields.IntField(default=0)
    day: SlotDays = fields.CharEnumField(SlotDays, default=SlotDays.All)
    active = fields.BooleanField(default=True)
    doctor: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="doctorslots")
    
class Appointments(models.Model):
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="userappointments")
    clinic: fields.ForeignKeyRelation[Clinic] = fields.ForeignKeyField(
        "models.Clinic", related_name="clinicappointments")
    requested_date = fields.DateField(null=True,blank=True)
    accepted_date = fields.DateField(null=True,blank=True)
    requested_slot: fields.ForeignKeyRelation[AppointmentSlots] = fields.ForeignKeyField(
        "models.AppointmentSlots", related_name="requestedappointments")
    accepted_slot : fields.ForeignKeyRelation[AppointmentSlots] = fields.ForeignKeyField(
        "models.AppointmentSlots", related_name="acceptedappointments",null=True,blank=True)
    status: AppointmentStatus = fields.CharEnumField(
        AppointmentStatus, default=AppointmentStatus.Pending)
    reason = fields.TextField(max_length=3000,null=True, blank=True)
    doctor: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="doctorappointments")
    
class Medicine(models.Model):
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    max_retial_price = fields.IntField(default=0)
    type: MedicineTypes = fields.CharEnumField(
        MedicineTypes, default=MedicineTypes.Capsules)
    title = fields.CharField(max_length=1000,unique=True)
    brand = fields.CharField(max_length=500,null=True,blank=True)
    active = fields.BooleanField(default=False)
    
    # class Meta:
    #     unique_together = (("title", "brand"), )

    
class Diagonsis(models.Model):
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    title = fields.CharField(max_length=1000, unique=True)
    active = fields.BooleanField(default=False)
    
    
class MedicalReports(models.Model):
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    title = fields.CharField(max_length=1000, unique=True)
    active = fields.BooleanField(default=False)
class ClinicReports(models.Model):
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    title = fields.CharField(max_length=1000, unique=True)
    active = fields.BooleanField(default=True)
    clinic: fields.ForeignKeyRelation[Clinic] = fields.ForeignKeyField(
        "models.Clinic", related_name="clinicavailablereports", null=True, blank=True)
    general_report: fields.ForeignKeyRelation[MedicalReports] = fields.ForeignKeyField(
        "models.MedicalReports", related_name="generalreports")
    price = fields.IntField(default=0)

class SubReports(models.Model):
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    status: AppointmentStatus = fields.CharEnumField(
        AppointmentStatus, default=AppointmentStatus.Pending)
    report: fields.ForeignKeyRelation[ClinicReports] = fields.ForeignKeyField(
        "models.ClinicReports", related_name="medicalclinicreports",null=True, blank=True)
    file = fields.TextField(null=True, blank=True, max_length=4000)
    expected_result = fields.DatetimeField(null=True,blank=True)
    report_name = fields.CharField(max_length=1200, null=True, blank=True)
    price = fields.IntField(default=0)


class LabReports(models.Model):
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    active = fields.BooleanField(default=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
    "models.User", related_name="userlabreports")
    clinic: fields.ForeignKeyRelation[Clinic] = fields.ForeignKeyField(
    "models.Clinic", related_name="cliniclabreports", null=True, blank=True)
    expected_result = fields.DatetimeField(null=True, blank=True)
    sub_reports: fields.ManyToManyRelation["SubReports"] = fields.ManyToManyField(
        "models.SubReports", related_name="mainreport")
    total_price = fields.IntField(default=0)

class PresMedicines(models.Model):
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    medicine: fields.ForeignKeyRelation[Medicine] = fields.ForeignKeyField(
        "models.Medicine", related_name="prescribedmedicines")
    diagonsis: fields.ForeignKeyRelation[Diagonsis] = fields.ForeignKeyField(
        "models.Diagonsis", related_name="diagonsismedicines")
    create_template = fields.BooleanField(default=False)
    medicine_type: MedicineTypes = fields.CharEnumField(
        MedicineTypes, default=MedicineTypes.Capsules)
    morning_count = fields.FloatField(default=0)
    afternoon_count = fields.FloatField(default=0)
    invalid_count = fields.FloatField(default=0)
    night_count = fields.FloatField(default=0)
    medicine_name = fields.CharField(max_length=1200,null=True,blank=True)
    diagonsisName = fields.CharField(max_length=1200,null=True,blank=True)
    qty_per_time = fields.FloatField(default=0)
    total_qty = fields.FloatField(default=0)
    command = fields.TextField(null=True, blank=True, max_length=4000)
    is_drug = fields.BooleanField(default=False)
    before_food = fields.BooleanField(default=False)
    is_given = fields.BooleanField(default=False)
    fromDate = fields.DateField(null=True, blank=True)
    toDate = fields.DateField(null=True, blank=True)
    days = fields.FloatField(default=0)
    
# class LabReports(models.Model):
#     created = fields.DatetimeField(auto_now_add=True)
#     updated = fields.DatetimeField(auto_now=True)
    
    
class Prescription(models.Model):
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="userprescriptions")
    clinic: fields.ForeignKeyRelation[Clinic] = fields.ForeignKeyField(
        "models.Clinic", related_name="clinicprescriptions",null=True,blank=True)
    doctor: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="doctorprescriptions",null=True,blank=True)
    medicines: fields.ManyToManyRelation["PresMedicines"] = fields.ManyToManyField(
        "models.PresMedicines", related_name="presmedicines")
    diagonsis_list: fields.ManyToManyRelation["Diagonsis"] = fields.ManyToManyField(
        "models.Diagonsis", related_name="presdiseases")
    medical_reports: fields.ManyToManyRelation["MedicalReports"] = fields.ManyToManyField(
        "models.MedicalReports", related_name="presreports")
    active = fields.BooleanField(default=True)
    create_template = fields.BooleanField(default=False)
    reason = fields.TextField(null=True, blank=True, max_length=4000)
    personal_prescription = fields.BooleanField(default=False)
    rating_taken = fields.BooleanField(default=False)
    receponist: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="recoptinistcreated", null=True, blank=True)
    gst_percentage = fields.FloatField(default=0)
    blood_sugar = fields.FloatField(default=0)
    blood_pressure = fields.FloatField(default=0)
    weight = fields.FloatField(default=0)
    invalid_till = fields.DateField(null=True, blank=True)
    doctor_fees = fields.FloatField(default=0)
    age = fields.IntField(default=0)
    next_visit = fields.DateField(null=True, blank=True)
    contains_drug = fields.BooleanField(default=False)
    is_template = fields.BooleanField(default=False)
    
class IssuePrescription(models.Model):
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="userrecievedprescriptions")
    clinic: fields.ForeignKeyRelation[Clinic] = fields.ForeignKeyField(
        "models.Clinic", related_name="clinicissuedprescriptions")
    prescription: fields.ForeignKeyRelation[Prescription] = fields.ForeignKeyField(
        "models.Prescription", related_name="issuedprescriptions")
    contains_drug = fields.BooleanField(default=False)
class PrescriptionTemplates(models.Model):
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    command = fields.TextField(max_length=2000,null=True,blank=True)
    diagonsis: fields.ForeignKeyRelation[Diagonsis] = fields.ForeignKeyField(
        "models.Diagonsis", related_name="templatediagonsis")
    medicines: fields.ManyToManyRelation["PresMedicines"] = fields.ManyToManyField(
        "models.PresMedicines", related_name="templatemedicines")
    active = fields.BooleanField(default=True)
    doctor_obj: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="doctortemplatess", null=True, blank=True)
    personal = fields.BooleanField(default=False)
    

    

@pre_save(Clinic)
async def signal_pre_save(
    sender: "Type[Clinic]", instance: Clinic, using_db, update_fields
) -> None:
    print(sender, instance, using_db, update_fields)
    
days = ["Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"]
@post_save(Clinic)
async def signal_post_save(
    sender: "Type[Clinic]",
    instance: Clinic,
    created: bool,
    using_db: "Optional[BaseDBAsyncClient]",
    update_fields: List[str],
) -> None:
    if not instance.created_subs:
        for day in days:
            timings_object = await ClinicTimings.create(day=day,timings=[])
            await instance.timings.add(timings_object)
        instance.created_subs = True
        inventry_obj = await Inventory.create(title=instance.name, types=instance.types)
        instance.inventory = inventry_obj
        await instance.save()
    print("successs")
    
    
@post_save(ClinicDoctors)
async def signal_post_doctor(
    sender: "Type[ClinicDoctors]",
    instance: ClinicDoctors,
    created: bool,
    using_db: "Optional[BaseDBAsyncClient]",
    update_fields: List[str],
) -> None:
    if not instance.subs:
        for day in days:
            timings_object = await ClinicTimings.create(day=day, timings=[])
            await instance.timings.add(timings_object)
        instance.subs = True
        await instance.save()
    print("successs")
    

    
