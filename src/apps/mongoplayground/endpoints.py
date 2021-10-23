from starlette.responses import JSONResponse
from .models import *
from .schemas import *
from fastapi import WebSocket, APIRouter, Body, Depends, HTTPException, Request, BackgroundTasks, status, UploadFile, File, Form, Depends , Query
from typing import List
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from src.config.mongo_conf import *
from .schemas import *
from .service import *
import os
from src.config.mongo_conf import virtual_database , local_database 
from src.config.settings import BASE_DIR, STATIC_ROOT , MEDIA_ROOT
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import pathlib
from bson import ObjectId
from bson.json_util import dumps
from bson import json_util
import shutil
import uuid
import json
mongo_router = APIRouter()

async def convert_mongo_list_json(cursor):
    return list(map(lambda row: {i: str(row[i]) if isinstance(row[i], ObjectId) else row[i] for i in row}, [i async for i in cursor]))
def convert_mongo_object(obj):
    return {i: str(obj[i]) if isinstance(obj[i], ObjectId) else obj[i] for i in obj}
@mongo_router.post("/createBooks")
async def create_books(data:Book):
    res = await virtual_database.capped.insert_one(data.dict())
    created_book =  virtual_database.capped.find({})
    
    # serialized_books =  list(map(lambda row: {i: str(row[i]) if isinstance(row[i], ObjectId) else row[i] for i in row}, books))
    return JSONResponse({"books":await convert_mongo_list_json(created_book)},status_code=200)
    # book = convert_book(created_book)
    # return JSONResponse(status_code=status.HTTP_201_CREATED, content=book)
async def get_product(product:Product) -> Product:
    return product
@mongo_router.post('/prac')
async def create_products(name: str = Form(...), description:str = Form(...),rating:int = Form(...),file: UploadFile = File(...),author:str = Form(...),man:List[str] = Form(...)):
    sample_uuid = uuid.uuid4()
    path = pathlib.Path(MEDIA_ROOT,f"product/{str(sample_uuid)+file.filename}")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with path.open('wb') as write:
        shutil.copyfileobj(file.file,write)

    if len(man) == 1:
        man = man[0].split(",")
    update = {'rating':rating,'name':name,'description':description,'author':author,'mm':man}
    print(update)
    return update
#    created_post = await virtual_database.product.insert_one(update)
#    created_post = await virtual_database.product.find_one({"_id":res.inserted_id})

@mongo_router.post('/uploadproducts')
async def upload_products(title: str = Form(...), description: str = Form(...), price: int = Form(...), file: UploadFile = File(...), shop: str = Form(...)):
    sample_uuid = uuid.uuid4()
    path = pathlib.Path(
        MEDIA_ROOT, f"products/{str(sample_uuid)+file.filename}")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # os.makedirs(os.path.dirname(path), exist_ok=True)
    with path.open('wb') as write:
        shutil.copyfileobj(file.file, write)
    res = await virtual_database.products.insert_one({"title": title, "shop": ObjectId(shop), 'price': price, 'image': str(path), 'description': description})
    obj = await virtual_database.products.find_one({"_id": res.inserted_id})
    return convert_mongo_object(obj)

@mongo_router.post('/createshops')
async def upload_products(name: str = Form(...), owner: str = Form(...), started_before: int = Form(...), file: UploadFile = File(...)):
    sample_uuid = uuid.uuid4()
    path = pathlib.Path(
        MEDIA_ROOT, f"shops/{str(sample_uuid)+file.filename}")
    # os.makedirs(os.path.dirname(path), exist_ok=True)
    with path.open('wb') as write:
        shutil.copyfileobj(file.file, write)
    res = await virtual_database.shops.insert_one({"name":name,"owner":owner,'started_before':started_before,'displayPicture':str(path)})
    obj = await virtual_database.shops.find_one({"_id": res.inserted_id})
    return convert_mongo_object(obj)
    
@mongo_router.get('/allshops')
async def get_shops(query: str = None):
    if query is None:
        shops = virtual_database.shops.find({})
    return JSONResponse({"books": await convert_mongo_list_json(shops)}, status_code=200)


@mongo_router.get('/shopsProducts')
async def get_shops(query: str = None):
    if query is None:
        products = virtual_database.shops.find({})
    if query is not None:
        products = virtual_database.shops.find({"shop":ObjectId(query)})
    return JSONResponse({"books": await convert_mongo_list_json(products)}, status_code=200)
    
    
@mongo_router.get('/path')
async def get_path() -> str:
    # print(BASE_DIR)
    s = pathlib.Path(__file__).parent.absolute()
    print(s.cwd())
    print(s.cwd())
    print(s.home())
    print(s)
    return STATIC_ROOT



