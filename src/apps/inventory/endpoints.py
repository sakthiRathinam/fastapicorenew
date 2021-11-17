from starlette.responses import JSONResponse
from .models import *
from .schema import *
from fastapi import WebSocket, APIRouter, Body, Depends, HTTPException, Request, BackgroundTasks, status, UploadFile, File, Form, Depends, Query
from typing import List
from fastapi import FastAPI, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from src.config.mongo_conf import *
from .schema import *
from .service import *
import os
from src.apps.prescriptionapp.models import Medicine
from src.config.mongo_conf import virtual_database, local_database
from src.config.settings import BASE_DIR, STATIC_ROOT, MEDIA_ROOT
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import pathlib
from bson import ObjectId
from bson.json_util import dumps
from bson import json_util
import shutil
import uuid
import json
medical_extra_router = APIRouter()

@medical_extra_router.post("/createMedicalInventory")
async def create_inventory(data: Inventory):
    data = data.dict()
    max_id = await virtual_database.inventory.find().sort("_id", -1).to_list(1)
    if max_id:
        data['_id'] = max_id[0]['_id'] + 1
    else:
        data['_id'] = 1
    data_obj = await virtual_database.inventory.insert_one(data)
    return {"success": "inventory added successfully"}
@medical_extra_router.post("/createClinicInventory")
async def create_inventory(data: Inventory):
    data = data.dict()
    max_id = await virtual_database.clinicinventory.find().sort("_id", -1).to_list(1)
    if max_id:
        data['_id'] = max_id[0]['_id'] + 1
    else:
        data['_id'] = 1
    data_obj = await virtual_database.inventory.insert_one(data)
    return {"success": "inventory added successfully"}



    

@medical_extra_router.post("/getInventory")
async def create_inventory(clinic: int):
    inv_obj = await virtual_database.inventory.find_one({"clinic": clinic}, {'medicines': {'$slice': [0, 5]}})
    return inv_obj





@medical_extra_router.delete("/deleteInventory")
async def delete_inventory(id: str):
    delete_obj = await virtual_database.inventory.delete_one({"_id": id})
    return "inventory deleted"

@medical_extra_router.delete("/deleteClinicInventory")
async def delete_inventory(id: str):
    delete_obj = await virtual_database.clinicinventory.delete_one({"_id": id})
    return "inventory deleted"
    
    
@medical_extra_router.post("/getClinicInventory")
async def create_inventory(clinic: int):
    inv_obj = await virtual_database.clinicinventory.find_one({"clinic": clinic}, {'medicines': {'$slice': [0, 5]}})
    return "inventory deleted"




@medical_extra_router.post('/addClinicMedicines')
async def update_inventory(data: AddMedicine):
    data = data.dict()
    inventory = data.pop('inventory')
    update_obj = await virtual_database.inventory.find_one({"_id": inventory})
    if data['main_medicine'] is None:
        data['main_medicine'] = await get_main_medicine()
    medicine_obj = await virtual_database.inventory.find(
        {"_id": inventory, "medicines.name": data['name']}).to_list(1)
    if medicine_obj:
        return "medicine already available kindly update dont add duplicate"
    # if update_obj.get('medicines') is not None:
    #     medicines = update_obj['medicines']
    #     medicines.append(data)
    # else:
    #     medicines = update_obj['medicines'] = [data]
    updating_obj = await virtual_database.inventory.update_one({"_id": inventory}, {"$push": {"medicines": data}})
    return "updated"

@medical_extra_router.post('/checkAvailablity')
async def check_availability(data: CheckAvailable):
    for medicine in data.medicines:
        check_obj = await virtual_database.clinicinventory.find_one({"clinic":data.clinic,"medicines.total_qty":{"$gte":medicine.quantity},"medicines.name":medicine.medicine})
        if check_obj:
            continue
        else:
            return JSONResponse({"available":False,"detail":f'{medicine.medicine} this medicine is not available'})
    return JSONResponse({"available": True, "detail": "all medicines are available"})
    



@medical_extra_router.post('/addMedicines')
async def update_inventory(data: AddMedicine):
    data = data.dict()
    inventory = data.pop('inventory')
    update_obj = await virtual_database.inventory.find_one({"_id": inventory})
    medicine_obj = await virtual_database.inventory.find(
        {"_id":inventory,"medicines.name": data['name']}).to_list(1)
    if medicine_obj:
        return "medicine already available kindly update dont add duplicate"
    # if update_obj.get('medicines') is not None:
    #     medicines = update_obj['medicines']
    #     medicines.append(data)
    # else:
    #     print("update")
    #     medicines = update_obj['medicines'] = [data]
    updating_obj = await virtual_database.inventory.update_one({"_id": inventory}, {"$push": {"medicines": data}})
    return "updated"

@medical_extra_router.post('/checkavailabilty')
async def medicine_availabilty(medicines:List[str],clinic:int=Body(...)):
    available = await virtual_database.inventory.find_one({"clinic": clinic, "medicines.name": {"$all": medicines}})
    if available:
        return {"success":"all required medicines are available in this shop"}
    return JSONResponse({"error":"some medicines are not available try some other shops"},status_code=500)

@medical_extra_router.delete('/deleteMedicine')
async def delete_medicine(medicine:str,clinic:int):
    deleted_obj = await virtual_database.inventory.update_one({'clinic': clinic}, {"$pull": {"medicines": {"name": medicine}}})
    if deleted_obj.modified_count:
        return "medicine object is deleted successfully"
    return JSONResponse({"error": "object does not exist"}, status_code=500)

@medical_extra_router.post('/updateMedicine')
async def update_medicine(data: NormalMedicine):
    data = data.dict()
    clinic = data.pop('clinic')
    deleted_obj = await virtual_database.inventory.update_one({'clinic': clinic}, {"$pull": {"medicines": {"name": data['name']}}})
    update_obj = await virtual_database.inventory.find_one({"clinic": clinic})
    if update_obj.get('medicines') is not None:
        medicines = update_obj['medicines']
        medicines.append(data)
    else:
        medicines = update_obj['medicines'] = [data]
    return "medicine updated successfully"


