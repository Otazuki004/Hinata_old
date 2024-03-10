import os
import sys
from pyrogram import Client
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
HANDLER = ["~",".","!","/","$"]
DEVELOPER_ID = set(int(x) for x in os.environ.get("DEVELOPER_ID", "").split())
MONGO_DB_URI = os.environ.get("MONGO_DB_URI")
VERSION = 0.001

# CREATING CLIENT
if len(BOT_TOKEN) > 150:
    bot = Client("Hyper-Games", session_string=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=dict(root="HyperGames/plugins"))
else:
    bot = Client("Hyper-Games", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=dict(root="HyperGames/plugins"))

# FUNCTION
async def developer(_, update, __):
    message=update
    if message.from_user.id in DEVELOPER_ID:
        return True
    else:
        return False
        
# DATABASE
MONGO_DB = MongoClient(MONGO_DB_URI) # Special Thanks To KoraXD For Giving This Codes!!
GAME_DATABASE = AsyncIOMotorClient(MONGO_DB_URI)["HYPER_GAMES"]
