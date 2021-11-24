import pymongo
import asyncio
import os
import motor.motor_asyncio
from src.config.mongo_conf import virtual_database

async def mongo_indexes():
    # try:
    await virtual_database.inventory.create_index([('clinic', pymongo.DESCENDING)], unique=True, background=True)
    await virtual_database.inventory.create_index([('medicines.name', pymongo.ASCENDING)], background=True)
    await virtual_database.clinicinventory.create_index([('clinic', pymongo.ASCENDING)], unique=True, background=True)
    await virtual_database.main_inventory.create_index([('clinic', pymongo.ASCENDING)], unique=True, background=True)
    await virtual_database.clinicracks.create_index([('clinic', pymongo.ASCENDING), ('title',pymongo.ASCENDING)], unique=True, background=True, sparse=True)
    await virtual_database.clinicracks.create_index([('rack', pymongo.ASCENDING), ('medicines.name', pymongo.ASCENDING)], unique=True, background=True, sparse=True)
    await virtual_database.clinicracks.create_index([('medicines.clinic', pymongo.ASCENDING), ('medicines.name', pymongo.ASCENDING)], unique=True, background=True, sparse=True)
    # except:
    #     raise Exception('some error occured')
    print("indexes added successfully")

# async def main():
#     asyncio.create_task(inventory_indexes())
    
    
# if __name__ == '__main__':
#     asyncio.run(main(),debug=True)
