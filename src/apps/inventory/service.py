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
        "data":await collection.find_one({"_id":id},{embedded_list:{"$slice":[offset,limit]}})
    }
    return to_send

def next_alpha_round(s):
    return chr((ord(s.upper())+1 - 65) % 26 + 65)

def next_alpha(s):
    return chr((ord(s.upper())+1))

async def get_next_sorted(collection: motor.motor_asyncio.AsyncIOMotorCollection, id: int, embedded_list: str,current_alpha:str):
    next_char = next_alpha(current_alpha)
    to_send = [{"character":next_char,"newHeader":True}]
    get_sorted = await collection.aggregate([{"$match": {"_id": inv}}, {"$unwind": "$medicines"}, {"$match": {"medicines.title": {
                                        "$regex": "^"+next_char, "$options": "i"}}}, {"$sort": {"medicines.title": 1}}, {"$skip": offset}, {"$limit": limit}]).to_list(length=None)
    if len(get_sorted) == 0 and next_char != "Z":
        await get_next_sorted()
    to_send.extend(get_sorted)
    return get_sorted
    
    
    
    
    
class AsyncIterator:
    def __init__(self, seq):
        self.iter = seq
    def __aiter__(self):
        return self
    async def __anext__(self):
        try:
            return next(self.iter)
        except StopIteration:
            raise StopAsyncIteration
