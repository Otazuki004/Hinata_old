from HyperGames import *
from HyperGames.Database.games import *
from pyrogram import Client, filters
import os
import logging
import pyrogram

# LOGGING
logging.basicConfig(
    format="[Hyper-Games] %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

PWD = f"{os.getcwd()}/" # GETTING CURRENT PATH

# START COMMAND
@Sophia.on_message(filters.command("start", prefixes=HANDLER), filters.private)
async def Start(_, message):
    AVAILABLE_USERS = await GET_AVAILABLE_USERS() # GETTING AVAILABLE USERS IN DATABASE
    USER_ID = message.from_user.id # GETTING MESSAGE FROM USER ID
    if USER_ID in AVAILABLE_USERS: # CHECKING USER IN DATABASE
        await message.reply_photo(photo="", caption=f"""
Hey, **{message.from_user.first_name}**🥰

HyperGames is a free bot with only purpose to entertaining users, you just need to add me to your group. Thats easy, No?

**VERSION**: None
**LAST UPDATE**: [here](https://t.me/Hyper_Speed0)

if you need any help [contact us](https://t.me/FutureCity005)!
""")
    else:
        await message.reply_text("""
Hey, **{message.from_user.first_name}**🥰

**Seems** looks like you have to account in HyperGames
Click button below to create a account!
""")

if __name__ == "__main__":
    bot.start() # STARTING CLIENT
    pyrogram.idle()
