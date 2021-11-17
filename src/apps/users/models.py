from tortoise import fields, models, Tortoise ,run_async
from tortoise.contrib.pydantic import pydantic_model_creator
from enum import Enum, IntEnum
from typing import List
import datetime
from tortoise.exceptions import NoValuesFetched
from tortoise.signals import post_delete, post_save, pre_delete, pre_save

from src.apps.base.additionalfields import StringArrayField

class Roles(str,Enum):
    Doctor = "Doctor"
    Patient = "Patient"
    Recoponist = "Recoponist"
    MedicalRecoponist = "MedicalRecoponist"
    PharmacyOwner = "PharmacyOwner"
    LabOwner = "LabOwner"
    Admin = "Admin"


class InventoryCategory(str, Enum):
    Doctor = "Doctor"
    MedicalStore = "MedicalStore"
    Clinic = "Clinic"
    Lab = "Lab"
class RazorPayPlans(str, Enum):
    Monthly = "Monthly"
    Quarterly = "Quarterly"
    Yearly = "Yearly"
    Halfly = "Halfly"
    Lab = "Lab"
class Sex(str, Enum):
    Male = "Male"
    Female = "Female"
    TransGender = "TransGender"
    Others = "Others"
    Dog = "Dog"
    

class Inventory(models.Model):
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    title = fields.CharField(max_length=400)
    types: InventoryCategory = fields.CharEnumField(
        InventoryCategory, default=InventoryCategory.Clinic)
class PermissionLevel(str, Enum):
    Admin = "Admin"
    Emp = "Emp"
    LowPermissions = "LowPermissions"
class Permissions(models.Model):
    app_name = fields.CharField(max_length=500, unique=True)
    created = fields.DatetimeField(auto_now_add=True)
    permission_level: PermissionLevel = fields.CharEnumField(
        PermissionLevel, default=PermissionLevel.Admin)
    updated = fields.DatetimeField(auto_now=True)
    permissions: fields.ReverseRelation["User"]
    

class ClinicVerification(models.Model):
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    name = fields.CharField(max_length=700, index=True)
    email = fields.CharField(max_length=800, null=True, blank=True)
    mobile = fields.CharField(max_length=20, null=True, blank=True)
    verified = fields.BooleanField(default=False)


class User(models.Model):
    """ Model user """
    username = fields.CharField(max_length=100, unique=True)
    email = fields.CharField(max_length=100, unique=True,null=True,blank=True)
    permissions: fields.ManyToManyRelation["Permissions"] = fields.ManyToManyField(
        "models.Permissions", related_name="permissions", through="user_permissions"
    )
    mobile = fields.CharField(max_length=15,null=True,blank=True)
    roles: Roles = fields.CharEnumField(Roles, default=Roles.Patient)
    sex: Sex = fields.CharEnumField(Sex, default=Sex.Male)
    password = fields.CharField(max_length=100)
    first_name = fields.CharField(max_length=100,default="")
    last_name = fields.CharField(max_length=100, null=True,default="")
    city = fields.CharField(max_length=800, null=True,default="")
    state = fields.CharField(max_length=800, null=True,default="")
    country = fields.CharField(max_length=800, null=True,default="")
    pincode = fields.CharField(max_length=800, null=True,default="")
    date_of_birth = fields.DateField(default=datetime.date.today())
    date_join = fields.DatetimeField(auto_now_add=True)
    address = fields.TextField(max_length=3000, null=True, default="")
    qualifications = StringArrayField(null=True,blank=True)
    specialization = StringArrayField(null=True,blank=True)
    health_issues = StringArrayField(null=True,blank=True)
    notificationIds = StringArrayField(null=True,blank=True)
    last_login = fields.DatetimeField(null=True)
    experience = fields.IntField(null=True,blank=True)
    is_active = fields.BooleanField(default=True)
    is_staff = fields.BooleanField(default=False)
    currently_active = fields.BooleanField(default=False)
    display_picture = fields.CharField(max_length=2000, default="")
    is_superuser = fields.BooleanField(default=False)
    avatar = fields.CharField(max_length=1000, null=True)
    personal_inventory = fields.BooleanField(default=False)
    created_subs = fields.BooleanField(default=False)
    inventory: fields.ForeignKeyRelation[Inventory] = fields.ForeignKeyField(
        "models.Inventory", related_name="personalinventories", null=True, blank=True)
    # social_accounts: fields.ReverseRelation['SocialAccount']
    def full_name(self) -> str:
        return self.first_name + self.last_name
    
    def age(self) -> int:
        if self.date_of_birth is not None:
            print("hereeee")
            year = 365.2425
            start_date = self.date_of_birth
            end_date = datetime.date.today()
            age = round((end_date - start_date).days // year)
            return age
        return 0
    
    class PydanticMeta:
        computed = ["full_name","age"]
        exclude = ('full_name',"age")


User_Pydantic = pydantic_model_creator(User, name="User", exclude=[
                                       'id', 'date_join', 'is_superuser', 'is_active','is_staff'])
Users_Pydantic = pydantic_model_creator(User,name="UserCreate",exclude_readonly=True,exclude=['id'])
UserIn_Pydantic = pydantic_model_creator(
    User, name="UserIn", exclude_readonly=True)


@post_save(User)
async def signal_post_doctor(
    sender: "Type[User]",
    instance: User,
    created: bool,
    using_db: "Optional[BaseDBAsyncClient]",
    update_fields: List[str],
) -> None:
    if not instance.created_subs:
        if instance.personal_inventory:
            inventry_obj = await Inventory.create(title=instance.username,types="Doctor")
            instance.created_subs = True
            instance.inventory = inventry_obj
            await instance.save()

    
Create_ClinicVerification = pydantic_model_creator(
    ClinicVerification, name="clinicverification", exclude=("id", "created", "updated", 'verified'))
GET_ClinicVerification = pydantic_model_creator(
    ClinicVerification, name="ClinicVerification")
