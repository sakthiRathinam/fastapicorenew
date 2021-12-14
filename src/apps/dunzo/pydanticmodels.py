from src.apps.dunzo.models import *
from tortoise.contrib.pydantic import pydantic_model_creator
GET_Cart = pydantic_model_creator(
    Cart, name="getcliniccarts")


# Create_MonthlyPlans = pydantic_model_creator(
#     MonthlyPlans, name="craetemonthlyplans", exclude=("id", "created", "updated"))
# GET_plans = pydantic_model_creator(
#     MonthlyPlans, name="monthlyplans")
