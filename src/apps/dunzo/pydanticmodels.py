from src.apps.dunzo.models import *
from tortoise.contrib.pydantic import pydantic_model_creator
Create_CreateUserOrder = pydantic_model_creator(
    CreateUserOrder, name="CreateUserOrder", exclude=("id", "created", "updated", "acceptedclinics", 'required_medicines', 'clinic'))
GET_CreateUserOrder = pydantic_model_creator(
    CreateUserOrder, name="CreateUserOrder")
GET_MedicalAccepted = pydantic_model_creator(
    MedicalAccepted, name="MedicalAccepted")
CREATE_MedicalAccepted = pydantic_model_creator(
    MedicalAccepted, name="MedicalAccepted")
# Create_MonthlyPlans = pydantic_model_creator(
#     MonthlyPlans, name="craetemonthlyplans", exclude=("id", "created", "updated"))
# GET_plans = pydantic_model_creator(
#     MonthlyPlans, name="monthlyplans")
