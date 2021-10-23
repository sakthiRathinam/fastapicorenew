from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib import fastapi
# from starlette.middleware.sessions import SessionMiddleware
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from src.config.tortoise_conf import TORTOISE_ORM as db_config
from src.config import settings
from src.apps import routers
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import logging
from src.config.mongo_conf import virtual_client,local_client
from fastapi_pagination import LimitOffsetPage, Page, add_pagination

fastapi.logging = logging.getLogger('uvicorn')
app = FastAPI(
    title="Core",
    description="FastAPI Core",
    version="0.1.0",
)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")
# app.add_middleware(
#     TrustedHostMiddleware, allowed_hosts=[
#         "192.168.29.98", '192.168.29.12', '192.168.29.242', 'localhost', '127.0.0.1']
# )
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    virtual_client.close()
    local_client.close()
    

@app.on_event("startup")
async def start_db():
    init_tortoise()
    add_pagination(app)

    


db_config["generate_schemas"]=False
db_config["add_exception_handlers"]=True

# app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.include_router(routers.api_router, prefix=settings.API_V1_STR)


# register_tortoise(app, config=db_config)
def init_tortoise():
    register_tortoise(
        app,
        db_url=settings.DATABASE_URI,
        modules={"models": settings.APPS_MODELS},
        generate_schemas=False,
        add_exception_handlers=True,
    )
    print("tortoise connected successfully")
    
def init_mongo():
    pass
    
