from HyperGames import *
from HyperGames.Database.games import *
from pyrogram import Client, filters
import os
import logging
import pyrogram
import random
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# LOGGING
logging.basicConfig(
    format="[Hyper-Games] %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

PWD = f"{os.getcwd()}/" # GETTING CURRENT PATH


# START COMMAND
@bot.on_message(filters.command("start", prefixes=HANDLER), filters.private)
async def Start(_, message):
    NO_ACCOUNT_TXT = f"""
Hey, **{message.from_user.first_name}**🥰

**Seems**, looks like you don't have a account in HyperGames
Click button below to create a account!
"""
    AVAILABLE_USERS = await GET_AVAILABLE_USERS() # GETTING AVAILABLE USERS IN DATABASE
    START_PICS = ["https://graph.org//file/cf28b09dde9e91d103eac.jpg","https://graph.org//file/e8f4e3ff506cce09b614b.jpg"]
    START_PICS = random.choice(START_PICS)
    USER_ID = message.from_user.id # GETTING MESSAGE FROM USER ID
    if USER_ID in AVAILABLE_USERS: # CHECKING USER IN DATABASE
        await message.reply_photo(photo=START_PICS, caption=f"""
Hey, **{message.from_user.first_name}**🥰

HyperGames is a free bot with only purpose to entertaining users, you just need to add me to your group. Thats easy, No?

**VERSION**: None
**LAST UPDATE**: [here](https://t.me/Hyper_Speed0)

if you need any help [contact us](https://t.me/FutureCity005)!
""")
    else:
        await message.reply_text(
            text=NO_ACCOUNT_TXT
        )

if __name__ == "__main__":
    bot.start() # STARTING CLIENT
    pyrogram.idle()
