from HyperGames import *
from HyperGames.Database.games import *
from pyrogram import Client, filters
import os
import logging
import pyrogram
import random
import time
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

PWD = f"{os.getcwd()}/" # GETTING CURRENT PATH

CREATE_AC_BUTTON = InlineKeyboardMarkup([[InlineKeyboardButton("Create Account 🏦", callback_data="ACCOUNT_CREATE")]])
CREATE_AC_BUTTON_AGAIN = InlineKeyboardMarkup([[InlineKeyboardButton("Join Again", callback_data="ACCOUNT_CREATE")]])
continue_button = InlineKeyboardMarkup([[InlineKeyboardButton("Continue", callback_data="ACCOUNT_CREATE_CONTINUE")]])
START_BUTTONS = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("» Help", callback_data="HELP")
    ],
    [
        InlineKeyboardButton("➕ Add me in your Group ➕", url="https://t.me/HyperGames0_bot?startgroup=start")
    ],
    [
        InlineKeyboardButton("» 𝗛ʏᴘᴇʀ 𝗦ᴘᴇᴇᴅ™", url="https://t.me/Hyper_Speed0")
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
HELP_TEXT = """
**• Help Section**

**• /start** - Start me
**• /help** - Get this
**• /profile** - Get your profile or reply a user to get their profile
**• /coins** - Get amount of coins you have
**• /send** - Send coins to another user
**• /bet** - Bet some coins
**• /setname** - USAGE: /setname <new name>, Set a new name, required `1999` coins
**• /setpfp** - Reply to a image and set new pfp, required `1000` coins
**• /fight** - Reply a user and fight, required 500 coins to both players
**• /daily** - Get 500 coins for everyday, you need add bot username in your bio to use it.
"""
BACK_HELP = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Go Back", callback_data="BACKINHELP")]])

# CALLBACK QUERY 
@bot.on_callback_query()
async def Callback_query(_, CallbackQuery):
    user_id = CallbackQuery.from_user.id
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
    elif CallbackQuery.data == "HELP":
        await CallbackQuery.edit_message_text(
            text=HELP_TEXT,
            reply_markup=BACK_HELP
        )
    elif CallbackQuery.data == "BACKINHELP":
        AVAILABLE_USERS = await GET_AVAILABLE_USERS()
        USER_ID = CallbackQuery.from_user.id
        if USER_ID in AVAILABLE_USERS:
            await CallbackQuery.edit_message_text(
                text=f"""
Hey, **{CallbackQuery.from_user.first_name}** 🥰
HyperGames is a free bot with the only purpose of entertaining users. You just need to add me to your group. That's easy, right?

**Version**: 0.001
**Last Update**: [Here](https://t.me/Hyper_Speed0)

If you need any help, [contact us](https://t.me/FutureCity005)!
""",
                reply_markup=START_BUTTONS
            )
    elif CallbackQuery.data.startswith("DELETE_AC"):
        callbackdata = CallbackQuery.data
        user_id = callbackdata.split("DELETE_AC_")[1]
        user_id = int(user_id)
        if not user_id == CallbackQuery.from_user.id:
            await CallbackQuery.answer("This is not for you!")
            return
        await REMOVE_USER(user_id)
        await CallbackQuery.edit_message_text(
            text="Thanks for using our product.",
            reply_markup=CREATE_AC_BUTTON_AGAIN
        )
    elif CallbackQuery.data.endswith("_BANK"):
        bank = CallbackQuery.data.split("_BANK")[0]
        LOG = await CREATE_USER_BANK_ACCOUNT(user_id, bank)
        if LOG == "SUCCESS":
            await CallbackQuery.edit_message_text(
                text="SUCCESS BRO")
        elif LOG == "USER_ALREADY_HAVE_ACCOUNT_IN_THIS_BANK":
            await CallbackQuery.edit_message_text("You have already account in this bank")
        elif LOG.startswith("ERROR"):
            await bot.send_message(user_id, LOG)
            


# START COMMAND
@bot.on_message(filters.command("start", prefixes=HANDLER))
async def Start(_, message):
    NO_ACCOUNT_TXT = f"""
Hey, **{message.from_user.first_name}** 🥰

**Seems**, looks like you don't have an account in HyperGames
Click the button below to create an account!
"""
    AVAILABLE_USERS = await GET_AVAILABLE_USERS() # GETTING AVAILABLE USERS IN DATABASE
    START_PICS = ["https://graph.org//file/cf28b09dde9e91d103eac.jpg","https://graph.org//file/e8f4e3ff506cce09b614b.jpg"]
    START_PICS = random.choice(START_PICS)
    USER_ID = message.from_user.id # GETTING MESSAGE FROM USER ID
    if USER_ID in AVAILABLE_USERS: # CHECKING USER IN DATABASE
        await message.reply_photo(photo=START_PICS, caption=f"""
Hey, **{message.from_user.first_name}** 🥰
HyperGames is a free bot with the only purpose of entertaining users. You just need to add me to your group. That's easy, right?

**Version**: 0.001
**Last Update**: [Here](https://t.me/Hyper_Speed0)

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
    try:
        bot.run() # STARTING CLIENT
    except Exception as e:
        if str(e).startswith("Telegram says: [420 FLOOD_WAIT_X]"):
            h = e
            h = h.split("Telegram says: [420 FLOOD_WAIT_X] - A wait of ")[1]
            h = h.split(""" seconds is required (caused by "auth.ImportBotAuthorization")""")[0]
            h = int(h)
            print(f"Bot is in flood wait of {h} seconds, its required, bot automatically starts after {h} seconds")
            time.sleep(h+2)
            print("BOT STARTING AFTER FLOOD WAIT")
            bot.run()
        else:
            print(e)
