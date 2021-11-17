import uuid
from fastapi import APIRouter, Depends, BackgroundTasks, Response, status, Request
from typing import List
from fastapi import HTTPException
from pydantic import BaseModel
from .service import *
from tortoise.query_utils import Q
from src.apps.auth.security import get_password_hash,verify_password
from src.apps.auth.permissions import get_user
from fastapi.security import APIKeyCookie
from fastapi import Body
from starlette.responses import Response, HTMLResponse
from starlette import status
from src.config.settings import SECRET_KEY
from src.apps.auth.models import Verification
from jose import jwt
from .models import *
from .schema import *
from datetime import datetime , timedelta , date
from starlette.responses import JSONResponse
# from starlette.requests import Request
from src.apps.auth.send_email import *
from src.apps.auth.schema import VerificationOut
cookie_sec = APIKeyCookie(name="session")

user_router = APIRouter()
@user_router.get('/users')
async def get_all_users():
    return await user_service.all()


@user_router.get('/getUser/{userid}')
async def getUser(userid:int):
    user = await User.get(id=userid).prefetch_related("permissions")
    permissions = [i.app_name async for i in user.permissions.all()]
    user_serialized = await User_Pydantic.from_tortoise_orm(user)
    return {"userData": user_serialized, "permissions": permissions}

@user_router.post('/login')
async def save_cookie_user(response: Response, request: Request, username: str = Body(...), password: str = Body(...), notificationId:Optional[str]=Body(...)):
    print(username,password)
    if username and password is not None:
        authenticate = await user_service.authenticate(username,password)
        if authenticate is not None:
            user = await User.get(username=username)
            user.currently_active = True
            if notificationId is not None:
                current_notification = notificationId
                if user.notificationIds is None:
                    user.notificationIds = [current_notification]
                if user.notificationIds is not None:
                    if current_notification not in user.notificationIds:
                        user.notificationIds.append(current_notification)
            await user.save()
            expire = date.today() + timedelta(days=35)
            token = jwt.encode(
                {"username": username, "expires": str(expire)}, SECRET_KEY)
            print(response)
            response.set_cookie("session", token)
            return {"success":"login successfully","user":user}
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid user or password"
            )
def get_current_login(session:str = Depends(cookie_sec)):
    try:
        data = jwt.decode(session, SECRET_KEY)
        print(data)
        date = data['expires'].split("-")
        expiry_date = datetime(int(date[0]),int(date[1]),int(date[2]))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication"
        )
    if expiry_date < datetime.now():
        print("heree")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Token Expires Login Again"
        )
    return data['username']
    
        
@user_router.get('/checkSession')
def check_session(session: str = Depends(get_current_login)) -> str:
    print(session,"imhereee")
    return "session available"



@user_router.get('/hashedpassword')
def hased_password(password:str=None):
    if password is not None:
        hashed = get_password_hash(password)
        print(verify_password(password,hashed))
        print(verify_password(str(password),hashed))
        print(verify_password(str(1234),hashed))
        return {"password":hashed}

@user_router.get('/verify')
async def verify_user(token: uuid.UUID):
    obj = await Verification.get(link=token.link).prefetch_related('user')
    if obj:
        user = await User.get(id=obj.user.id)
        user.is_active = True
        user.save()
        await Verification.get(link=token.link).delete()
        return JSONResponse({"SUCCESS: ACTIVATED"},status_code=200)
    return JSONResponse({"error":"link is not avaialable"},status_code=500)





    

@user_router.get('/logout')
async def logout(response: Response, request:Request,session: str = Depends(get_current_login)):
    user = await User.get(username=session)
    user.currently_active = False
    if 'notificationId' in request.headers:
        print("heree")
        current_notification = request.headers['notificationId']
        if user.notificationIds is not None:
            if current_notification  in user.notificationIds:
                    user.notificationIds.remove(current_notification)
    await user.save()
    response.delete_cookie("session")
    return {"success":"user logout successfully"}
    
    

# @user_router.get('/printusers')
# async def get_all_users() -> None:
#     users = User.all()
#     async for user in users:
#         print(user.username)
#     user =await User.first()
#     print(user.username)
#     return None


@user_router.post("/signup", response_model=UserIn_Pydantic)
async def create_user(user: User_Pydantic,tasks:BackgroundTasks,response:Response):
    if await User.filter(Q(username=user.username)|Q(email=user.email)).exists():
        user = await User.filter(Q(username=user.username) | Q(email=user.email)).first()
        if  user.is_active:
            return JSONResponse({"error":"user already exists"},status_code=500)
        verification_link = await Verification.create(user=user)
        tasks.add_task(
            send_account_activate, user.email, user.username, user.password, verification_link.link
        )
        return JSONResponse({"res": "underprocesss"}, status_code=201)
    user_create = await user_service.create_user(user)
    user_obj = await User.get(username=user.username)
    verification_link =await Verification.create(user=user_obj)
    tasks.add_task(
        send_account_activate, user.email, user.username, user.password, verification_link.link
    )
    return JSONResponse({"res":"underprocesss"},status_code=201)


@user_router.post("/createUser", response_model=UserIn_Pydantic)
async def create_user(user: User_Pydantic,tasks:BackgroundTasks,response:Response):
    if await User.filter(Q(username=user.username)|Q(email=user.email)).exists():
        user = await User.filter(Q(username=user.username) | Q(email=user.email)).first()
        if  user.is_active:
            return JSONResponse({"error":"user already exists"},status_code=500)
        return JSONResponse({"user": "usercreated"}, status_code=201)
    user_create = await user_service.create_user(user)
    return JSONResponse({"user":"usercreated"},status_code=201)
    


async def something_print():
    print("awefawfawef")
    return  "awfawefawef"

@user_router.get('/playrequest/{item}')
def play_request(request: Request,item:int):
    print(request)
    print(request.query_params)
    print(request.path_params)
    print(request.query_params['path'])


@user_router.get('/searchUsers')
async def search_users(role: Roles, name: str, user : str=Depends(get_current_login)):
    toReturn = await User.filter(roles=role, first_name__istartswith=name).only('id','username','first_name','last_name')
    return toReturn[:5]
@user_router.get('/searchMobileUsers')
async def search_users(role: Roles, mobile: str, user : str=Depends(get_current_login)):
    toReturn = await User.filter(roles=role, mobile__istartswith=mobile).only('id', 'username', 'first_name', 'last_name', 'mobile', 'date_of_birth', 'health_issues', 'sex')
    return toReturn[:5]


@user_router.post('/addClinicverification')
async def add_medicines(data: Create_ClinicVerification = Body(...)):
    add_medicine = await clinic_verify.create(data)
    return {"medicine": "clinic verfication registered successfully you will receive a call within 3 working days"}


@user_router.delete('/deleteClinicverification')
async def delete_medicines(id: int):
    await clinic_verify.delete(id=id)
    return {"success": "deleted"}


@user_router.put('/editClinicverification')
async def update_medicines(id: int, data: Create_ClinicVerification = Body(...)):
    await clinic_verify.update(data, id=id)
    return {"success": "updated"}


@user_router.put('/filterClinicverification')
async def filter_medicines(data: GET_ClinicVerification = Body(...)):
    await clinic_verify.filter(**data.dict(exclude_unset=True))
    return {"success": "updated"}


async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@user_router.get('/checkdepends')
async def get_depends(commons:dict = Depends(common_parameters)) -> dict:
    return commons


@user_router.get('/authtoken')
async def get_depends(user:User = Depends(get_user)):
    return await User_Pydantic.from_tortoise_orm(user)
