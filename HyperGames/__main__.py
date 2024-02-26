from HyperGames import *
from HyperGames.Database.games import *
from pyrogram import Client, filters
import os
import logging
import pyrogram
import random
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

PWD = f"{os.getcwd()}/" # GETTING CURRENT PATH

CREATE_AC_BUTTON = InlineKeyboardMarkup([[InlineKeyboardButton("Create Account 🏦", callback_data="ACCOUNT_CREATE")]])
continue_button = InlineKeyboardMarkup([[InlineKeyboardButton("Continue", callback_data="ACCOUNT_CREATE_CONTINUE")]])
START_BUTTONS = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("Help", callback_data="HELP"),
        InlineKeyboardButton("Hyper Speed ™", callback_data="ACCOUNT_CREAThdE")
    ]
])
registration_text = """
**🎮 Welcome To Hyper Games ©**

**• ACCOUNT REGISTRATION 🎮**
- Join the Hyper Games community now!
- No personal data required.
- Your journey begins with a simple command: /continue.

**• By Clicking "Continue", you agree to our Terms and Conditions.**
"""
setupcomplete_text = "**Nice**, you have joined in HyperGames™, Play games and enjoy, in this process you got 1000 coins as reward"

@bot.on_callback_query()
async def Create_Account(_, CallbackQuery):
    if CallbackQuery.data == "ACCOUNT_CREATE":
        AVAILABLE_USERS = await GET_AVAILABLE_USERS()
        user_id = CallbackQuery.from_user.id
        if user_id in AVAILABLE_USERS:
            return await CallbackQuery.edit_message_text("You have account already.")
        await CallbackQuery.edit_message_text(
            text=registration_text,
            reply_markup=continue_button
        )
    elif CallbackQuery.data == "ACCOUNT_CREATE_CONTINUE":
        AVAILABLE_USERS = await GET_AVAILABLE_USERS()
        user_id = CallbackQuery.from_user.id
        if user_id in AVAILABLE_USERS:
            return await CallbackQuery.edit_message_text("You have account already.")
        await ADD_NEW_USER(user_id)
        await ADD_COINS(user_id, 1000)
        await CallbackQuery.edit_message_text(setupcomplete_text)

# START COMMAND
@bot.on_message(filters.command("start", prefixes=HANDLER))
async def Start(_, message):
    print("Start triggered")
    NO_ACCOUNT_TXT = f"""
Hey, **{message.from_user.first_name}**🥰

**Seems**, looks like you don't have an account in HyperGames
Click the button below to create an account!
"""
    AVAILABLE_USERS = await GET_AVAILABLE_USERS() # GETTING AVAILABLE USERS IN DATABASE
    START_PICS = ["https://graph.org//file/cf28b09dde9e91d103eac.jpg","https://graph.org//file/e8f4e3ff506cce09b614b.jpg"]
    START_PICS = random.choice(START_PICS)
    USER_ID = message.from_user.id # GETTING MESSAGE FROM USER ID
    if USER_ID in AVAILABLE_USERS: # CHECKING USER IN DATABASE
        await message.reply_photo(photo=START_PICS, caption=f"""
Hey, **{message.from_user.first_name}**🥰

HyperGames is a free bot with the sole purpose of entertaining users. You just need to add me to your group. That's easy, right?

**VERSION**: None
**LAST UPDATE**: [here](https://t.me/Hyper_Speed0)

If you need any help, [contact us](https://t.me/FutureCity005)!
""", reply_markup=START_BUTTONS)
    else:
        await message.reply_text(
            text = NO_ACCOUNT_TXT,
            reply_markup = CREATE_AC_BUTTON
        )

# LOGGING
logging.basicConfig(
    format="[Hyper-Games] %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

if __name__ == "__main__":
    bot.run() # STARTING CLIENT
    
