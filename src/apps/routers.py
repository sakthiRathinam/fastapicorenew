from fastapi import APIRouter
from src.apps.users.views import user_router
from src.apps.auth.views import auth_router
from src.apps.websockets.endpoints import socket_router
from src.apps.mongoplayground.endpoints import mongo_router
from src.apps.videostreaming.endpoints import stream_router
from src.apps.prescriptionapp.endpoints import clinto_router
from src.apps.razorpay.endpoints import razor_router
from src.apps.dunzo.endpoints import dunzo_router
from src.apps.inventory.endpoints import medical_extra_router
api_router = APIRouter()
api_router.include_router(user_router, prefix='/users', tags=["users"])
api_router.include_router(auth_router, prefix='/login', tags=["auth"])
api_router.include_router(socket_router, prefix='/sockets', tags=["sockets"])
api_router.include_router(dunzo_router, prefix='/dunzo', tags=["dunzo"])
# api_router.include_router(mongo_router, prefix='/mongo', tags=["mongo"])
# api_router.include_router(stream_router, prefix='/videos', tags=["video"])
api_router.include_router(clinto_router, prefix='/clinto', tags=["clinto"])
api_router.include_router(razor_router, prefix='/razor', tags=["razor"])
api_router.include_router(medical_extra_router,
                          prefix='/medicalInventory', tags=["medical"])
