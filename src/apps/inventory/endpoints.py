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
from src.apps.users.views import get_current_login, get_session_current_login
from src.apps.prescriptionapp.models import Medicine
from src.config.mongo_conf import virtual_database, local_database
from src.config.settings import BASE_DIR, STATIC_ROOT, MEDIA_ROOT
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from .service import get_sequence, get_embedded_size, mongo_limited_data_embedded, mongo_limited_data_normal
import pathlib
from src.config.settings import MAIN_MICROSERVICE_HOST
from bson import ObjectId
from bson.json_util import dumps
from bson import json_util
import shutil
import uuid
import aiohttp
import json
medical_extra_router = APIRouter(
    dependencies=[Depends(get_session_current_login)])

@medical_extra_router.post("/createMedicalInventory")
async def create_inventory(data: Inventory):
    data = data.dict()
    data['_id'] = await get_sequence("inventory")
    data_obj = await virtual_database.inventory.insert_one(data)
    return {"success": "inventory added successfully","id":data['_id']}

def next_alpha(s):
    return chr((ord(s.upper())+1))


@medical_extra_router.post('/updateMedicine')
async def update_medicine(data: NormalMedicine):
    data = data.dict()
    clinic = data.pop('inventory')
    deleted_obj = await virtual_database.inventory.update_one({'_id': inventory}, {"$pull": {"medicines": {"name": data['name']}}})
    update_obj = await virtual_database.inventory.find_one({"clinic": clinic})
    if update_obj.get('medicines') is not None:
        medicines = update_obj['medicines']
        medicines.append(data)
    else:
        medicines = update_obj['medicines'] = [data]
    return "medicine updated successfully"

async def create_main_medicine(data:NormalMedicine,csrf:str,medical:bool):
    host = f"{MAIN_MICROSERVICE_HOST}/api/v1/clinto/addMedicalMedicines"
    data_dict = data.dict()
    data_dict['is_medical'] = medical
    async with aiohttp.ClientSession(headers={"csrf": csrf}) as session:
        async with session.post(host, json=data_dict) as res:
            medicine_obj = await res.json()
            return medicine_obj['id']
        


    
@medical_extra_router.post('/addMedicalMedicines')
async def update_inventory(data: NormalMedicine,request:Request):
    data_dict = data.dict()
    csrf_token = request.headers.get('csrf')
    if data_dict['main_medicine'] is None:
        data_dict['main_medicine'] = await create_main_medicine(data,csrf_token,True)
    inventory = data_dict.pop('inventory')
    update_obj = await virtual_database.inventory.find_one({"_id": inventory})
    medicine_obj = await virtual_database.inventory.find(
        {"_id": inventory, "medicines.name": data_dict['name']}).to_list(1)
    if medicine_obj:
        return "medicine already available kindly update dont add duplicate"
    updating_obj = await virtual_database.inventory.update_one({"_id": inventory}, {"$push": {"medicines": data_dict}})
    return {"success":"medicine added successfully"}

@medical_extra_router.put('/updateMedicalMedicines')
async def update_medicine(data: NormalMedicine):
    data = data.dict()
    inventory = data.pop('inventory')
    deleted_obj = await virtual_database.inventory.update_one({'_id': inventory}, {"$pull": {"medicines": {"name": data['name']}}})
    update_obj = await virtual_database.inventory.update_one({'_id': inventory}, {"$push": {"medicines": data}})
    if update_obj.modified_count:
        return "medicine updated successfully"
    else:
        raise HTTPException(
            status_code=status.HTTP_500_BAD_REQUEST, detail="something went wrong,server error"
        )
@medical_extra_router.delete('/deleteMedicalMedicines')
async def delete_medicine(inv:int,medicine:str):
    deleted_obj = deleted_obj = await virtual_database.inventory.update_one({'_id': inv}, {"$pull": {"medicines": {"name": medicine}}})
    if deleted_obj.modified_count:
        return "medicine deleted successfully"
    else:
        raise HTTPException(
            status_code=status.HTTP_500_BAD_REQUEST, detail="medicine not found in the inventory try again"
        )
@medical_extra_router.get("/getMedicalMedicines")
async def get_medical_medicines(inv:int,starting_letter:Optional[str]="A",limit:Optional[int]=10,offset:Optional[int]=0):
    to_send = {
        "previousoffset":offset,
        "data": [{"character": starting_letter, "newHeader": True}],
        "number_of_data" : 0,
        "previouschar":None,
        "nextavailable":True
    }
    limit = limit
    get_sorted = await virtual_database.inventory.aggregate([{"$match": {"_id": inv}}, {"$unwind": "$medicines"}, {"$match": {"medicines.name": {"$regex": "^"+starting_letter, "$options": "i"}}}, {"$sort": {"medicines.name": 1}}, {"$skip": offset},{"$limit": limit}]).to_list(length=None)
    print(get_sorted)
    to_send['data'].extend(get_sorted)
    print(len(get_sorted))
    print(to_send['data'])
    if len(get_sorted) == 0 and starting_letter.lower() == "z":
        to_send['nextavailable'] = False
        to_send['previouschar'] = starting_letter
        to_send['number_of_data'] = 0
        return to_send
    if len(get_sorted) < 10 and starting_letter.lower() != "z":
        to_send['previousoffset'] = 0
        to_send['number_of_data'] += len(get_sorted)
        limit -= len(get_sorted)
        if len(get_sorted) == 0:
            to_send['data'].pop()
        next_char = next_alpha(starting_letter)
        to_send['data'].append(
            {"character": next_char, "newHeader": True})
        while limit:
            get_sorted = await virtual_database.inventory.aggregate([{"$match": {"_id": inv}}, {"$unwind": "$medicines"}, {"$match": {"medicines.name": {"$regex": "^"+next_char, "$options": "i"}}}, {"$sort": {"medicines.title": 1}}, {"$skip": 0}, {"$limit": limit}]).to_list(length=None)
            if len(get_sorted) == 0:
                if len(to_send['data']) != 0:
                    to_send['data'].pop()
            else:
                to_send['data'].extend(get_sorted)
                to_send['number_of_data'] += len(get_sorted)
                limit -= len(get_sorted)
            if limit !=0 and next_char.lower() == "z" and limit != 10:
                to_send['previouschar'] = next_char
                to_send['nextavailable'] = False
                return to_send
            if limit == 10 and next_char.lower() == "z":
                to_send['nextavailable'] = False
                to_send['previouschar'] = next_char
                return to_send
            next_char = next_alpha(next_char)
            to_send['data'].append(
                {"character": next_char, "newHeader": True})
            
    to_send['data'].extend(get_sorted)
    to_send['previouschar'] = starting_letter
    to_send['number_of_data'] = 10
    return to_send
            
    # if len(get_sorted) == 0:
    #     to_send['previousoffset'] = 0
    #     current_sorted = get_next_sorted(db.inventory, inv, current_alpha)
    #     if len(current_sorted) == 1:
    #         raise HTTPException(
    #             status_code=status.HTTP_500_BAD_REQUEST, detail="end of the medicines"
    #         )
    #     else:
    #         to_send['data'] = current_sorted
    #         return current_sorted
    # else:
    #     return 
            
    
@medical_extra_router.post("/createClinicInventory")
async def create_clinic_inventory(data: ClinicInventory):
    data = data.dict()
    data['_id'] = await get_sequence("main_inventory")
    data_obj = await virtual_database.main_inventory.insert_one(data)
    return {"success": "inventory added successfully", "data_obj": data_obj.inserted_id}
    

@medical_extra_router.post("/createClinicRacks")
async def create_clinic_racks(data: ClinicRack):
    data = data.dict()
    data['_id'] = await get_sequence("clinicracks")
    data_obj = await virtual_database.clinicracks.insert_one(data)
    updating_obj = await virtual_database.main_inventory.update_one({"_id": data['inventory']}, {"$push": {"racks":{"title":data['title'],"id":data_obj.inserted_id}}})
    return {"success": "rack added successfully"}


@medical_extra_router.post('/createClinicOrders')
async def create_orders(data: ClinicOrders):
    data = data.dict()
    data['expected_delivery'] = str(data['expected_delivery'])
    data['_id'] = await get_sequence("clinicorders")
    data_obj = await virtual_database.clinicorders.insert_one(data)
    return {"success": "orders added successfully", "id": data['_id']}
# @medical_extra_router.post("/")


@medical_extra_router.get('/getClinicOrders')
async def get_orders(inv: int,limit: Optional[int] = 10, offset: Optional[int] = 0):
    limited_data = await db.clinicorders.find({"inventory": 4}, {"orderedMedicines": 0}).skip(offset).limit(limit).to_list(length=None)
    return limited_data
    
@medical_extra_router.get('/getMinimumOrders')
async def get_minimum(inv:int):
    min_medicines = await virtual_database.clinicracks.aggregate([{"$match": {"inventory": inv}}, {"$unwind": "$medicines"}, {"$match": {"$expr": {"$gt": ["$medicines.min_qty", "$medicines.total_qty"]}}}]).to_list(length=None)
    to_send = []
    for medicine in min_medicines:
        medicine_obj = dict()
        medicine_obj['name'] = medicine['medicines']['name']
        medicine_obj['item'] = medicine['medicines']
        medicine_obj['status'] = "Pending"
        medicine_obj['subbox_per_boxes'] = medicine['medicines']['subbox_per_boxes']
        medicine_obj['piece_per_subboxes'] = medicine['medicines']['piece_per_subboxes']
        medicine_obj['medicine_type'] = medicine['medicines']['medicine_type']
        medicine_obj['main_medicine'] = medicine['medicines']['main_medicine']
        minus_quantity = medicine['medicines']['min_qty'] -  medicine['medicines']['total_qty']
        medicine_obj['total_qty'] = minus_quantity
        if medicine['medicines']['medicine_type'] == "Tablet" or medicine['medicines']['medicine_type'] == 'Capsules':
            total_strips = minus_quantity // medicine['medicines']['piece_per_subboxes']
            medicine_obj['total_boxes'] = round(
                total_strips // medicine['medicines']['subbox_per_boxes'])
            medicine_obj['total_subboxes'] = round(total_strips %
                                                   medicine['medicines']['piece_per_subboxes'])
            medicine_obj['total_loose'] = round(minus_quantity %
                                                medicine['medicines']['piece_per_subboxes'])
        else:
            medicine_obj['total_boxes'] = minus_quantity // medicine['medicines']['subbox_per_boxes']
            medicine_obj['total_subboxes'] = round(minus_quantity %
                                                   medicine['medicines']['subbox_per_boxes'])
            
        to_send.append(medicine_obj)
    return to_send    
        

@medical_extra_router.put('/updateOrders')
async def add_minimum(data: UpdateOrders):
    data_dict = data.dict()
    current_order_pk = data_dict.pop('order')
    current_order = await db.clinicorders.update_one({"_id":current_order_pk},{"$set":data_dict})
    find_order = await db.clinicorders.find_one({"_id": current_order_pk}, {"orderedMedicines": 0})
    if current_order.modified_count:
        return "order updated succcessfully"
    

@medical_extra_router.put('/updateMedicineStatus')
async def update_medicine_status(data: List[OrderMedicines], order: int, inventory: int, status: OrderStatus):
    data_dict = [sub.dict() for sub in data]
    name_list = [name.name for name in data]
    if status != "Received":
        db_update_all = await db.clinicorders.update_one({"_id": order}, {"$set": {"orderedMedicines.$[orderedMedicines].status": status}}, upsert=True, array_filters=[{"orderedMedicines.name": {"$in": name_list}}])
        return "status changed to all medicines successfully"
    else:
        db_update_all = await db.clinicorders.update_one({"_id": order}, {"$set": {"orderedMedicines.$[orderedMedicines].status": status}}, upsert=True, array_filters=[{"orderedMedicines.name": {"$in": name_list}}])
        updated_count = 0
        inventory_data = await db.clinicracks.find({"inventory":inventory,"medicines.name":{"$in":name_list}},{
            "medicines":{"$elemMatch":{"name":{"$in":name_list}}}}).to_list(length=None)
        for inv_medicine in inventory_data:
            for medicine in inv_medicine['medicines']:
                print(medicine)
                for order_medicine in data_dict:
                    if medicine['name'] == order_medicine['name']:
                        minus_quantity = medicine['total_qty'] + order_medicine['total_qty']
                        medicine_obj = {"total_subboxes": 0, "total_boxes": 0, "total_loose": 0, "total_qty":minus_quantity}
                        if medicine['medicine_type'] == "Tablet" or medicine['medicine_type'] == 'Capsules':
                            total_strips = minus_quantity // medicine['piece_per_subboxes']
                            medicine_obj['total_boxes'] = round(
                                total_strips // medicine['subbox_per_boxes'])
                            medicine_obj['total_subboxes'] = round(total_strips %
                                                                medicine['piece_per_subboxes'])
                            medicine_obj['total_loose'] = round(minus_quantity %
                                                medicine['piece_per_subboxes'])
                        else:
                            medicine_obj['total_boxes'] = minus_quantity // medicine['medicines']['subbox_per_boxes']
                            medicine_obj['total_subboxes'] = round(minus_quantity %
                                                   medicine['subbox_per_boxes'])
                        update_obj = await db.clinicracks.update_one({"_id": inv_medicine['_id']}, {"$set": {"medicines.$[medicines].total_boxes": medicine_obj['total_boxes'], "medicines.$[medicines].total_loose": medicine_obj['total_loose'], "medicines.$[medicines].total_subboxes": medicine_obj['total_subboxes'], "medicines.$[medicines].total_qty": medicine_obj['total_qty']}},upsert=True,array_filters=[{"medicines.name":medicine['name']}])
                        if update_obj.modified_count:
                            updated_count +=1
        return {"success":"medicines updated successfully","updated_count":updated_count}
    
    
@medical_extra_router.put('/updateUsedMedicines')
async def update_used_medicines(data:UsedMedicinesUpdate):
    data_dict = data.dict()
    print(data_dict,"imawegawegewageg")
    inventory = data_dict.pop('inventory')
    name_list = [medicine.name for medicine in data.medicines]
    inventory_data = await db.clinicracks.find({"inventory":inventory,"medicines.name":{"$in":name_list}},{
        "medicines":{"$elemMatch":{"name":{"$in":name_list}}}}).to_list(length=None)
    medicines_missing = []
    medicines_there = []
    updated_count = 0
    create_used = []
    for inv_medicine in inventory_data:
        for medicine in inv_medicine['medicines']:
            for order_medicine in data_dict['medicines']:
                if medicine['name'] == order_medicine['name']:
                    if medicine['total_qty'] < order_medicine['total_qty']:
                        medicines_missing.append(medicine['name'])
                    else:
                        minus_quantity = medicine['total_qty'] - order_medicine['total_qty']
                        medicine_obj = {"total_subboxes": 0, "total_boxes": 0, "total_loose": 0, "total_qty":minus_quantity}
                        if medicine['medicine_type'] == "Tablet" or medicine['medicine_type'] == 'Capsules':
                            total_strips = minus_quantity // medicine['piece_per_subboxes']
                            medicine_obj['total_boxes'] = round(
                                total_strips // medicine['subbox_per_boxes'])
                            medicine_obj['total_subboxes'] = round(total_strips %
                                                                medicine['piece_per_subboxes'])
                            medicine_obj['total_loose'] = round(minus_quantity %
                                                medicine['piece_per_subboxes'])
                        else:
                            medicine_obj['total_boxes'] = minus_quantity // medicine['medicines']['subbox_per_boxes']
                            medicine_obj['total_subboxes'] = round(minus_quantity %
                                                    medicine['subbox_per_boxes'])
                        update_obj = await db.clinicracks.update_one({"_id": inv_medicine['_id']}, {"$set": {"medicines.$[medicines].total_boxes": medicine_obj['total_boxes'], "medicines.$[medicines].total_loose": medicine_obj['total_loose'], "medicines.$[medicines].total_subboxes": medicine_obj['total_subboxes'], "medicines.$[medicines].total_qty": medicine_obj['total_qty']}},upsert=True,array_filters=[{"medicines.name":medicine['name']}])
                        
                        current_sequence = await get_sequence("usedmedicines")
                        create_used = await virtual_database.usedmedicines.insert_one({"_id":current_sequence,"total_qty":minus_quantity,"name":medicine['name'],"type":medicine['medicine_type'],"diagonsis":order_medicine['diagonsis'],"main_medicine":order_medicine['main_medicine'],"used":str(datetime.now()),"inventory":inventory})
                        if update_obj.modified_count:
                            updated_count += 1
    return {"success":True,"updated_count":updated_count}

@medical_extra_router.put('/reteriveUsedMedicines')
async def reterive_used_medicines(data:UsedMedicinesUpdate):
    data_dict = data.dict()
    inventory = data_dict.pop('inventory')
    name_list = [medicine.name for medicine in data.medicines]
    
    inventory_data = await db.clinicracks.find({"inventory":inventory,"medicines.name":{"$in":name_list}},{
        "medicines":{"$elemMatch":{"name":{"$in":name_list}}}}).to_list(length=None)
    medicines_missing = []
    medicines_there = []
    updated_count = 0
    create_used = []
    for inv_medicine in inventory_data:
        for medicine in inv_medicine['medicines']:
            for order_medicine in data_dict['medicines']:
                if medicine['name'] == order_medicine['name']:
                    if medicine['total_qty'] < order_medicine['total_qty']:
                        medicines_missing.append(medicine['name'])
                    else:
                        minus_quantity = medicine['total_qty'] - order_medicine['total_qty']
                        medicine_obj = {"total_subboxes": 0, "total_boxes": 0, "total_loose": 0, "total_qty":minus_quantity}
                        if medicine['medicine_type'] == "Tablet" or medicine['medicine_type'] == 'Capsules':
                            total_strips = minus_quantity // medicine['piece_per_subboxes']
                            medicine_obj['total_boxes'] = round(
                                total_strips // medicine['subbox_per_boxes'])
                            medicine_obj['total_subboxes'] = round(total_strips %
                                                                medicine['piece_per_subboxes'])
                            medicine_obj['total_loose'] = round(minus_quantity %
                                                medicine['piece_per_subboxes'])
                        else:
                            medicine_obj['total_boxes'] = minus_quantity // medicine['medicines']['subbox_per_boxes']
                            medicine_obj['total_subboxes'] = round(minus_quantity %
                                                    medicine['subbox_per_boxes'])
                        update_obj = await db.clinicracks.update_one({"_id": inv_medicine['_id']}, {"$set": {"medicines.$[medicines].total_boxes": medicine_obj['total_boxes'], "medicines.$[medicines].total_loose": medicine_obj['total_loose'], "medicines.$[medicines].total_subboxes": medicine_obj['total_subboxes'], "medicines.$[medicines].total_qty": medicine_obj['total_qty']}},upsert=True,array_filters=[{"medicines.name":medicine['name']}])
                        current_sequence = await get_sequence("usedmedicines")
                        create_used = await virtual_database.usedmedicines.insert_one({"_id":current_sequence,"total_qty":minus_quantity,"name":medicine['name'],"type":medicine['medicine_type'],"diagonsis":order_medicine['diagonsis'],"main_medicine":order_medicine['main_medicine'],"used":str(datetime.now()),"inventory":inventory})
                        if update_obj.modified_count:
                            updated_count += 1
    return {"success":True,"updated_count":updated_count}


@medical_extra_router.get('/getUsedMedicines')
async def get_used_medicines(inventory:int,limit:Optional[int]=10,offset:Optional[int]=0):
    get_used_data_mongo = await mongo_limited_data_normal(db.usedmedicines,count_filter={"inventory":inventory},filter_objs={"inventory":inventory},limit=limit,offset=offset)
    return get_used_data_mongo
@medical_extra_router.delete('/deleteUsedMedicines')
async def get_used_medicines(id:int):
    
    return get_used_data
    
                        
                        
@medical_extra_router.put('/changeRack')
async def change_rack(data: ChangeRack):
    medicine_dict = data.medicine.dict()
    delete_med = await db.clinicracks.update_one({"_id":data.current_rack},{"$pull":{"medicines":{"name":medicine_dict['name']}}})
    update_rack = await db.clinicracks.update_one({"_id":data.transfer_rack},{"$push":{"medicines":medicine_dict}})
    return "medicine rack changed successfully"
    

@medical_extra_router.get('/searchRacks')
async def search_racks(title:str,inv:int):
    search_medicines = await db.clinicracks.aggregate([{"$match": {"inventory": inv, "title": {"$regex": "^"+str(title), "$options": "i"}}},{"$project":{"medicines":0}},{"$limit": 5}]).to_list(length=None)
    return search_medicines

@medical_extra_router.put('/updateOrderMedicine')
async def add_minimum(data: OrderMedicines,order:int):
    data_dict = data.dict()
    print(data_dict)
    current_order_pk = order
    current_order_pull = await db.clinicorders.update_one({"_id": order}, {"$pull": {"orderedMedicines": {"name": data_dict['name']}}})
    current_order_push = await db.clinicorders.update_one({"_id": order}, {"$push": {"orderedMedicines": data_dict}})
    if current_order_push.modified_count:
        return "order medicine updated succcessfully"
    

@medical_extra_router.get('/getOrderMediciens')
async def add_minimum(order: int):
    ordered_medicines = await virtual_database.clinicorders.find_one({"_id":order})
    return ordered_medicines

@medical_extra_router.delete('/deleteClinicOrders')
async def add_minimum(order: int):
    ordered_medicines = await virtual_database.clinicorders.delete_one({"_id":order})
    return "order deleted successfully"
    


    

@medical_extra_router.post("/createRackMedicines")
async def create_clinic_racks(request:Request,data: ClinicMedicine):
    data_dict = data.dict()
    csrf_token = request.headers.get('csrf')
    inv_obj = await virtual_database.main_inventory.update_one({"_id": data_dict['inventory']}, {"$addToSet": {"available_medicines": data_dict['name']}})
    if not inv_obj.modified_count:
        raise HTTPException(
            status_code=status.HTTP_500_BAD_REQUEST, detail="medicine already available update that or delete and add"
            )
    if data_dict['main_medicine'] is None:
        data_dict['main_medicine'] = await create_main_medicine(data, csrf_token,False)
    rack_id = data_dict.pop('rack')
    updating_obj = await virtual_database.clinicracks.update_one({"_id": rack_id}, {"$push": {"medicines": data_dict}})
    return {"updated":"medicine added successfully"}

@medical_extra_router.put('/updateRackMedicines')
async def update_rack_medicines(data:ClinicMedicine):
    data = data.dict()
    rack_id = data.pop("rack")
    deleted_obj = await virtual_database.clinicracks.update_one({"_id":rack_id},{"$pull":{"medicines":{"name":data['name']}}})
    updated_obj = await virtual_database.clinicracks.update_one({"_id": rack_id}, {"$push": {"medicines": data}})
    if updated_obj.modified_count:
        return "medicine updated successfully"
    

@medical_extra_router.delete('/deleteRackMedicines')
async def delete_medicines(inventory:int,name:str,rack:int):
    delete_set = await virtual_database.main_inventory.update_one({"_id": inventory}, {"$pull": {"available_medicines": name}})
    delete_medicine = await virtual_database.clinicracks.update_one({"_id": rack}, {"$pull": {"medicines": {"name": name}}})
    return "medicine deleted successfully"


@medical_extra_router.delete('/deleteRack')
async def delete_medicines(rack: int,inventory:int):
    delete_rack = await virtual_database.clinicracks.delete_one({"_id":rack})
    delete_rack_inventory = await virtual_database.main_inventory.update_one({"_id":inventory},{"$pull":{"racks":{"id":rack}}})
    return "rack deleted successfully"


# @medical_extra_router.get('/getRackMedicines')
# async def get_racks(rack:int,limit:Optional[int]=10,offset:Optional[int]=0):
#     limited_data = await mongo_limited_data_embedded(virtual_database.clinicracks, rack, "medicines",limit=limit,offset=offset)
#     return limited_data

@medical_extra_router.get('/getRackMedicines')
async def get_rack_medicines(rack:int,limit:Optional[int]=10,offset:Optional[int]=0):
    limited_data = await mongo_limited_data_embedded(virtual_database.clinicracks, rack, "medicines", limit=limit, offset=offset)
    return limited_data
    
@medical_extra_router.get('/getRacks')
async def get_racks(inventory:int,limit:Optional[int]=10,offset:Optional[int]=0):
    limited_data = await mongo_limited_data_embedded(virtual_database.main_inventory, inventory, "racks", limit=limit, offset=offset)
    return limited_data
    
    
@medical_extra_router.post('/checkMedicineAvailablityy')
async def medicine_availabilty(medicines: List[str]=Body(...), clinic: int = Body(...)):
    medicines_list = [{"$elemMatch":{"name":{"$regex":"^"+medicine,"$options":"i"}}}for medicine in medicines]
    available = await virtual_database.inventory.find_one({"clinic": clinic, "medicines": {"$all": medicines_list}})
    if available:
        return {"success": "all required medicines are available in this shop"}
    return JSONResponse({"error": "some medicines are not available try some other shops"}, status_code=500)


@medical_extra_router.get('/searchMedicalMedicines')
async def medicine_availabilty(inv:int,search:str):
    search_medicines = await db.inventory.aggregate([{"$match": {"_id":inv}},{"$unwind":"$medicines"},{"$match":{"medicines.name":{"$regex":"^"+str(search),"$options":"i"}}},{"$limit":5}]).to_list(length=None)
    return search_medicines    
@medical_extra_router.get('/searchClinicMedicines')
async def medicine_availabilty(inv:int,search:str):
    search_medicines = await db.clinicracks.aggregate([{"$match": {"inventory": inv}}, {"$unwind": "$medicines"}, {"$match": {"medicines.name": {"$regex": "^"+str(search), "$options": "i"}}}, {"$limit": 5}]).to_list(length=None)
    return search_medicines    
    

@medical_extra_router.post("/createClinicSubInventory")
async def create_inventory(data: Inventory):
    data = data.dict()
    max_id = await virtual_database.clinicinventory.find().sort("_id", -1).to_list(1)
    if max_id:
        data['_id'] = max_id[0]['_id'] + 1
    else:
        data['_id'] = 1
    data_obj = await virtual_database.inventory.insert_one(data)
    pdating_obj = await virtual_database.inventory.update_one({"_id": inventory}, {"$push": {"racks": data['title']}})
    return {"success": "rack added successfully"}

@medical_extra_router.post("/getInventory")
async def create_inventory(clinic: int):
    inv_obj = await virtual_database.inventory.find_one({"clinic": clinic}, {'medicines': {'$slice': [0, 5]}})
    return inv_obj

@medical_extra_router.post("/getClinicInventory")
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
    return "inventory items"


@medical_extra_router.post("/getClinicInventory")
async def create_inventory(clinic: int):
    pass

@medical_extra_router.post("/getClinicMedicines")
async def create_rack(rackno:str):
    pass
    
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

@medical_extra_router.post('/checkRemoveAvailablity')
async def check_availability(data: CheckAvailable):
    for medicine in data.medicines:
        check_obj = await virtual_database.clinicinventory.find_one({"clinic":data.clinic,"medicines.total_qty":{"$gte":medicine.quantity},"medicines.name":medicine.medicine,"medicines.medicine_type":medicine.medicine_type},{"medicines":{"$elemMatch":{"name":medicine.medicine,"medicine_type":medicine.medicine_type}}})
        if check_obj:
            medicine_obj = check_obj['medicines'][0]
            if medicine_obj['medicine_type'] == "Capsules" or medicine_obj['medicine_type'] == "Tablet":
                minus_quantity = medicine_obj['total_qty'] - medicine.quantity
                total_strips = minus_quantity // medicine_obj.piece_per_subboxes
                medicine_obj['total_boxes'] = round(
                    total_strips // medicine_obj.subbox_per_boxes)
                medicine_obj['total_subboxes'] = round(total_strips %
                                        medicine_obj.strips_per_boxes)
                medicine_obj['total_loose'] = round(minus_quantity %
                                    medicine_obj.medicines_per_strips)
                deleted_obj = await virtual_database.clinicinventory.update_one({'clinic': clinic}, {"$pull": {"medicines": {"name": medicine, "medicine_type": medicine.medicine_type}}})
                if deleted_obj:
                    updating_obj = await virtual_database.clinicinventory.update_one({"_id": inventory}, {"$push": {"medicines": medicine_obj}})
            else:
                minus_quantity = medicine_obj['total_qty'] - medicine.quantity
                medicine_obj['total_subboxes'] = minus_quantity // medicine_obj.piece_per_subboxes
                medicine_obj['total_loose'] = round(minus_quantity %
                                                    medicine_obj.medicines_per_strips)
                deleted_obj = await virtual_database.clinicinventory.update_one({'clinic': clinic}, {"$pull": {"medicines": {"name": medicine, "medicine_type": medicine.medicine_type}}})
                if deleted_obj:
                    updating_obj = await virtual_database.clinicinventory.update_one({"_id": inventory}, {"$push": {"medicines": medicine_obj}})
        else:
            return JSONResponse({"available":False,"detail":f'{medicine.medicine} this medicine is not available'})
    return JSONResponse({"available": True, "detail": "all medicines are available"})
    

@medical_extra_router.post('/checkClinicAvailablity')
async def check_availability(data: CheckAvailable):
    for medicine in data.medicines:
        check_obj = await virtual_database.clinicinventory.find_one({"clinic": data.clinic, "medicines.total_qty": {"$gte": medicine.quantity}, "medicines.name": medicine.medicine, "medicines.medicine_type": medicine.medicine_type}, {"medicines": {"$elemMatch": {"name": medicine.medicine, "medicine_type": medicine.medicine_type}}})
        if check_obj:
            pass
        else:
            return JSONResponse({"available": False, "detail": f'{medicine.medicine} this medicine is not available'})
    return JSONResponse({"available": True, "detail": "all medicines are available"})

@medical_extra_router.post('/checkQuantityAvailablity')
async def check_availability(data: CheckAvailable):
    for medicine in data.medicines:
        check_obj = await virtual_database.inventory.find_one({"clinic": data.clinic, "medicines.total_qty": {"$gte": medicine.quantity}, "medicines.name": medicine.medicine, "medicines.medicine_type": medicine.medicine_type}, {"medicines": {"$elemMatch": {"name": medicine.medicine, "medicine_type": medicine.medicine_type}}})
        if check_obj:
            pass
        else:
            return JSONResponse({"available": False, "detail": f'{medicine.medicine} this medicine is not available'})
    return JSONResponse({"available": True, "detail": "all medicines are available"})


@medical_extra_router.post('/checkMedicineAvailablity')
async def medicine_availabilty(medicines:List[str],clinic:int=Body(...)):
    available = await virtual_database.inventory.find_one({"clinic": clinic, "medicines.name": {"$all": medicines}})
    if available:
        return {"success":"all required medicines are available in this shop"}
    return JSONResponse({"error":"some medicines are not available try some other shops"},status_code=500)
    




@medical_extra_router.post('/addClinicMedicines')
async def update_inventory(data: ClinicMedicine):
    data = data.dict()
    inventory = data.pop('inventory')
    update_obj = await virtual_database.clinicinventory.find_one({"_id": inventory})
    medicine_obj = await virtual_database.clinicinventory.find(
        {"_id":inventory,"medicines.name": data['name']}).to_list(1)
    
    if medicine_obj:
        return "medicine already available kindly update dont add duplicate"
    # if update_obj.get('medicines') is not None:
    #     medicines = update_obj['medicines']
    #     medicines.append(data)
    # else:
    #     print("update")
    #     medicines = update_obj['medicines'] = [data]
    updating_obj = await virtual_database.clinicinventory.update_one({"_id": inventory}, {"$push": {"medicines": data}})
    return "updated"

@medical_extra_router.delete('/deleteMedicine')
async def delete_medicine(medicine:str,clinic:int):
    deleted_obj = await virtual_database.inventory.update_one({'clinic': clinic}, {"$pull": {"medicines": {"name": medicine}}})
    if deleted_obj.modified_count:
        return "medicine object is deleted successfully"
    return JSONResponse({"error": "object does not exist"}, status_code=500)

@medical_extra_router.delete('/deleteClinicMedicine')
async def delete_medicine(medicine:str,clinic:int):
    deleted_obj = await virtual_database.clinicinventory.update_one({'clinic': clinic}, {"$pull": {"medicines": {"name": medicine}}})
    if deleted_obj.modified_count:
        return "medicine object is deleted successfully"
    return JSONResponse({"error": "object does not exist"}, status_code=500)




