import os
import sys
import time
from Hinata.Database.main import *
from pyrogram import *
from pyrogram.types import *
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
    bot = Client("Hyper-Games", session_string=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=dict(root="Hinata/plugins"))
else:
    bot = Client("Hyper-Games", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=dict(root="Hinata/plugins"))

# FUNCTION
async def developer(_, client, update):
    message=update
    if message.from_user.id in DEVELOPER_ID:
        return True
    else:
        return False

        
# DATABASE
MONGO_DB = MongoClient(MONGO_DB_URI) # Special Thanks To KoraXD For Giving This Codes!!
GAME_DATABASE = AsyncIOMotorClient(MONGO_DB_URI)["HYPER_GAMES"]

@bot.on_message(filters.text, group=1)
async def fukkers(_, m: Message):
  spammer = await GAME_DATABASE.flood.find_one({'user_id': m.from_user.id})
  if not m.from_user.id in await GET_AVAILABLE_USERS():
    return 
  if not spammer:
    await GAME_DATABASE.flood.insert_one({'user_id': m.from_user.id, 'flood': 1, 'time': time.time(), 'mute': False})
  else:
    if spammer['mute']:
      if int(time.time() - spammer['time']) >= 600:
        await GAME_DATABASE.flood.delete_one(spammer)
        await m.reply_text("-_-")
    else:
      mf = spammer['flood'] + 1
      if mf >= 5 and (time.time() - spammer['time']) >= 3:
        await GAME_DATABASE.flood.update_one(spammer, {'$set': {'mute': True, 'flood': mf, 'time': time.time()}})
        await m.reply_text("You are spaming so can't use the bot for 10mins")
      else:
        await GAME_DATABASE.flood.update_one(spammer, {'$set': {'flood': mf}})
          
async def is_spamed(_, __, m: Message):
  bitch = await GAME_DATABASE.flood.find_one({'user_id': m.from_user.id})
  if bitch:
    if bitch['mute']:
      return False
  return True


floodfilter = filters.create(is_spamed)
