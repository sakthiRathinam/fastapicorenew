from .models import *
from .schema import *
from fastapi import APIRouter, Body, Depends, HTTPException, Request , BackgroundTasks ,status
from typing import List
from pydantic import BaseModel
from .schema import Token, Msg, VerificationOut
from .jwt import create_token
from fastapi.security import OAuth2PasswordRequestForm
from .send_email import send_test_email
from src.apps.users import service, schema
auth_router = APIRouter()


@auth_router.post('/access-token',response_model=Token)
async def create_access_token(userform : OAuth2PasswordRequestForm = Depends()):
    user = await service.user_service.authenticate(username=userform.username,password=userform.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return create_token(user.id)


@auth_router.post('/test-email',status_code=status.HTTP_202_ACCEPTED)
async def send_mail(email:str,task:BackgroundTasks) -> None:
    task.add_task(
        send_test_email, email_to=email
    )
    return {"msg": "Password recovery email sent"}


    