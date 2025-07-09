# Current db mock can be used for tests
from beanie import PydanticObjectId, init_beanie
from fastapi import FastAPI

# from mongomock import MongoClient
from mongomock_motor import AsyncMongoMockClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.core.models.models import BEANIE_DOCUMENTS




global DB_INSTANCE
DB_INSTANCE = None


async def start_db_client(app: FastAPI):
    # If there is anything to do @ db when the app start, should be implemented here
    # Like reseting or checking some state
    if settings.ENV == "TEST":
        db = get_db()
        await init_beanie(database=db, document_models=BEANIE_DOCUMENTS)
        await setup_hardcoded_db(db)

    else:
        db = get_db()


async def stop_db_client(app: FastAPI):
    global DB_INSTANCE
    if settings.ENV == "TEST":
        DB_INSTANCE = None


async def initialize_beanie(db):
    await init_beanie(database=db, document_models=BEANIE_DOCUMENTS)


def get_db() -> dict:
    global DB_INSTANCE
    if settings.ENV in ["LOCAL", "TEST"]:
        if DB_INSTANCE is None:
            DB_INSTANCE = AsyncMongoMockClient()["techmatch"]
        return DB_INSTANCE
    else:
        if DB_INSTANCE is None:
            DB_INSTANCE = AsyncIOMotorClient(settings.DB_URL)[settings.DB_NAME]
        return DB_INSTANCE


async def setup_hardcoded_db(db):
    # This function is used to setup the db with some hardcoded data
    # It should be used only in TEST env
    # For example, to create some users or other entities that are needed for tests
    pass  # Implement any hardcoded data setup here if needed