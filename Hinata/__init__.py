import os
import sys
import time

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

cmds = ["/wager", "/wager@SylvieArcadeBot"]
@bot.on_message(filters.all, group=1)
async def fukkers(_, m: Message):
  spammer = await GAME_DATABASE.floodo.find_one({'user_id': m.from_user.id})
  if not m.text in cmds:
    return 
  if not spammer:
    await GAME_DATABASE.floodo.insert_one({'user_id': m.from_user.id, 'flood': 1, 'mute': False})
  else:
    if spammer['mute']:
      if int(time.time() - spammer['time']) >= 120:
        await GAME_DATABASE.floodo.update_one(spammer, {'$set': {'mute': False, 'flood': 0}})
        await m.reply_text("`Your 2 Minutes Ignored Was Removed`")
    else:
      mf = spammer['flood'] + 1
      if mf > 15:
        await GAME_DATABASE.floodo.update_one(spammer, {'$set': {'mute': True, 'flood': mf, 'time': time.time()}})
        await m.reply_text("`You've Been Ignored For 2 Minutes`")
      else:
        await GAME_DATABASE.floodo.update_one(bitch, {'$set': {'flood': mf}})
          
async def is_spamed(_, __, m: Message):
  bitch = await GAME_DATABASE.floodo.find_one({'user_id': m.from_user.id})
  if bitch:
    if bitch['mute']:
      return False
  return True


floodfilter = filters.create(is_spamed)
