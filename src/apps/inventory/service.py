import pymongo
import asyncio
import os
import motor.motor_asyncio
from src.config.mongo_conf import virtual_database as db
from typing import Optional


async def get_sequence(sequencename: str) -> int:
    sequence = await db.counters.find_one_and_update(filter={"_id": sequencename}, update={"$inc": {"current_sequence": 1}}, new=True)
    return sequence['current_sequence']


async def get_embedded_size(collection: motor.motor_asyncio.AsyncIOMotorCollection, id:int,embedded_list: str) -> int:
    get_aggeration =  collection.aggregate([{"$match":{"_id":id}},{"$project":{"total_count":{"$size":"$"+embedded_list}}}])
    try:
        obj = await get_aggeration.next()
        return obj['total_count']
    except:
        return 0


async def mongo_limited_data_embedded(collection: motor.motor_asyncio.AsyncIOMotorCollection, id: int, embedded_list: str,limit:Optional[int]=10,offset:Optional[int]=0):
    total_count = await get_embedded_size(collection, id, embedded_list)
    to_send = {
        "total_count":total_count,
        "next":True if limit + offset < total_count else False,
        "prev":True if offset > 0  else False,
        "data":await collection.find_one({"_id":id},{"medicines":{"$slice":[offset,limit]}})
    }
    
