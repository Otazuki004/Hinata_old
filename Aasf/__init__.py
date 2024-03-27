import time

from typing import Union
from config import *

from motor.motor_asyncio import AsyncIOMotorClient as MongoClient

from pyrogram import *
from pyrogram.types import *

app = Client(
    'Hinata',
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN
)
app.start()
mongo_client = MongoClient(MONGO_DB_URL)
db = mongo_client.Hinata
bot_username = "Hinata7Bot" # without @

# spam module 
cmds = ["bet"]
prefixes = ["/", "?", "$", "!", "#", "@"]
@bot.on_message(filters.text, group=1)
async def autospam(_, m: Message):
  spammer = await db.flood.find_one({'user_id': m.from_user.id})
  if not m.text.split()[0][1:] or m.text.split()[0][1:] + f"@{bot_username}" in cmds:
    return 
  if not spammer:
    await db.flood.insert_one({'user_id': m.from_user.id, 'flood': 1, 'time': time.time(), 'mute': False})
  else:
    if spammer['mute']:
      if int(time.time() - spammer['time']) >= 600:
        await db.flood.delete_one(spammer)
        await m.reply_text("`Your 10 Minutes Ignored Was Removed`")
    else:
      total = spammer['flood'] + 1
      if total >= 5 and (time.time() - spammer['time']) >= 3:
        await db.flood.update_one(spammer, {'$set': {'mute': True, 'flood': total, 'time': time.time()}})
        await m.reply_text("`You've Been Ignored For 10 Minutes`")
      else:
        await db.flood.update_one(spammer, {'$set': {'flood': total}})
          
async def is_spamed(_, __, m: Message):
  user = await db.flood.find_one({'user_id': m.from_user.id})
  if user:
    if user['mute']:
      return False
  return True


floodfilter = filters.create(is_spamed)

def get_command(comm: Union[list, str]):
  res = list()
  if isinstance(comm, str):
    res.extend([comm, f"{comm}@{bot_username}"])
  if isinstance(comm, list):
    for com in comm:
      res.extend([com, f"{com}@{bot_username}"])
  return filters.command(res, prefixes=prefixes) & floodfilter
