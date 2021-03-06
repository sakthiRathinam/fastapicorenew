import pymongo
import asyncio
import os
import motor.motor_asyncio
from src.config.mongo_conf import virtual_database as db


async def counters():
    await db.counters.insert_one({"_id": "main_inventory", "current_sequence": 0})
    await db.counters.insert_one({"_id": "inventory", "current_sequence": 0})
    await db.counters.insert_one({"_id": "clinicracks", "current_sequence": 0})
    await db.counters.insert_one({"_id": "clinicorders", "current_sequence": 0})
    await db.counters.insert_one({"_id": "clinicinventory", "current_sequence": 0})
    await db.counters.insert_one({"_id": "usedmedicines", "current_sequence": 0})
    await db.counters.insert_one({"_id": "clinics", "current_sequence": 0})
    await db.counters.insert_one({"_id": "chatgroups", "current_sequence": 0})
    await db.counters.insert_one({"_id": "chatmessages", "current_sequence": 0})
