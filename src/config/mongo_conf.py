import motor.motor_asyncio
from src.config.settings import VIRTUAL_MONGO_URL, LOCAL_MONGO_URL

virtual_client = motor.motor_asyncio.AsyncIOMotorClient(VIRTUAL_MONGO_URL)

virtual_database = virtual_client['sharma']


local_client = motor.motor_asyncio.AsyncIOMotorClient(LOCAL_MONGO_URL)

local_database = local_client['sharma']


