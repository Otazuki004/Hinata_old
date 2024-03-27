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

# LIST COMMANDS IN BOT
get_commands = await bot.get_bot_commands()

commands = []

for x in get_commands:
    if not x == "start" or not x == "help":
        commands.append(x)

# SPAM CONTROLER
@bot.on_message(filters.text, group=1)
async def spam_controler(_, m: Message):
  spammer = await GAME_DATABASE.flood.find_one({'user_id': m.from_user.id})
  msg = message.text.split()[0][1:])
  msg.lower()
  if msg not in commands:
    return
  if not spammer:
    await GAME_DATABASE.flood.insert_one({'user_id': m.from_user.id, 'flood': 1, 'time': time.time(), 'mute': False})
  else:
    if spammer['mute']:
      if int(time.time() - spammer['time']) >= 600:
        await GAME_DATABASE.flood.delete_one(spammer)
        await m.reply_text("`Your 10 Minutes Ignored Was Removed`")
    else:
      spam_usr = spammer['flood'] + 1
      if spam_usr >= 5 and (time.time() - spammer['time']) >= 3:
        await GAME_DATABASE.flood.update_one(spammer, {'$set': {'mute': True, 'flood': mf, 'time': time.time()}})
        await m.reply_text("`You've Been Ignored For 10 Minutes`")
      else:
        await GAME_DATABASE.flood.update_one(spammer, {'$set': {'flood': mf}})
          
async def is_spamed(_, __, m: Message):
  baka = await GAME_DATABASE.flood.find_one({'user_id': m.from_user.id})
  if baka:
    if baka['mute']:
      return False
  return True
    
floodfilter = filters.create(is_spamed)
