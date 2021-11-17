import pymongo
import asyncio
import os
import motor.motor_asyncio
from src.config.mongo_conf import virtual_database

async def mongo_indexes():
    # try:
    await virtual_database.inventory.create_index([('clinic', pymongo.DESCENDING)], unique=True, background=True)
    await virtual_database.inventory.create_index([('medicines.name', pymongo.DESCENDING)],background=True)
    # await virtual_database.inventory.drop_index("medicines.name_-1")
    # except:
    #     raise Exception('some error occured')
    print("indexes added successfully")

# async def main():
#     asyncio.create_task(inventory_indexes())
    
    
# if __name__ == '__main__':
#     asyncio.run(main(),debug=True)
