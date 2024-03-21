from Hinata import *
from Hinata.Database.main import *
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
**🎮 Welcome To Account Registration**

**• ACCOUNT REGISTRATION 🎮**
- Join the Hinata community now!
- No personal data required.
- Your journey begins with clicking: continue.

**• By Clicking "Continue", you agree to our Terms and Conditions.**
"""
setupcomplete_text = "Your account has been created successfully, Check the commands using /help!"
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
**👋🏻 Hey {CallbackQuery.from_user.first_name}-san!**

__🎮 I'm your Hinata Game Bot, ready to be your loyal ally, just like Hinata is to Naruto! ❤️ Let's dive into exciting games and mysteries together! 👀 Ready for an epic adventure? 💫__

**🗯️ Check Below Buttons For More!**
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
    elif CallbackQuery.data == "NO":
        await CallbackQuery.message.delete()
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
    elif CallbackQuery.data.startswith("DEPOSIT_COINS"):
        data = CallbackQuery.data
        user = data.split("\nUSER: ")[1]
        user = int(user.split("\n")[0])
        if not user == CallbackQuery.from_user.id:
            return await CallbackQuery.answer("This is not for you!")
        coins = data.split("\nCOINS: ")[1]
        coins = int(coins.split("\n")[0])
        bank = data.split("\n")[3]
        await CallbackQuery.edit_message_text("`Depositing...`")
        log = await DEPOSIT_COINS(user, coins, bank)
        if log == "USER_HAVE_NO_ACCOUNT_IN_THAT_BANK":
            await CallbackQuery.edit_message_text("You don't have account in the selected bank!")
        elif log == "SUCCESS":
            await CallbackQuery.edit_message_text(f"**{coins}** has successfully deposited to bank")
        elif log.startswith("ERROR"):
            await CallbackQuery.edit_message_text(log)
    elif CallbackQuery.data.startswith("WITHDRAW_COINS"):
        data = CallbackQuery.data
        user = data.split("\nUSER: ")[1]
        user = int(user.split("\n")[0])
        if not user == CallbackQuery.from_user.id:
            return await CallbackQuery.answer("This is not for you!")
        coins = data.split("\nCOINS: ")[1]
        coins = int(coins.split("\n")[0])
        if coins <= 0:
            return await CallbackQuery.edit_message_text("Coins must be positive integer!.")
        bank = data.split("\n")[3]
        await CallbackQuery.edit_message_text("`Withdrawing...`")
        log = await WITHDRAW_COINS_FROM_BANK(user, coins, bank)
        if log == "USER_HAVE_NO_ACCOUNT_IN_THAT_BANK":
            await CallbackQuery.edit_message_text("You don't have account in the selected bank!")
        elif log == "NOT_ENOUGH_COINS_IN_BANK":
            balance = await GET_USER_COINS_FROM_BANK(user, bank)
            await CallbackQuery.edit_message_text(f"You don't have {coins} in the specific bank, your bank account balance is {balance}!")
        elif log == "SUCCESS":
            await CallbackQuery.edit_message_text(f"**{coins}** has successfully withdrawed to you!")
        elif log.startswith("ERROR"):
            await CallbackQuery.edit_message_text(log)


# START COMMAND
@bot.on_message(filters.command("start", prefixes=HANDLER))
async def Start(_, message):
    NO_ACCOUNT_TXT = f"""
You don't have a account, create your new account using clicking button below!
"""
    AVAILABLE_USERS = await GET_AVAILABLE_USERS() # GETTING AVAILABLE USERS IN DATABASE
    START_PICS = ["https://telegra.ph/file/7c9b3c398bca04f56b1a9.jpg","https://telegra.ph/file/c08f34182779d3461367d.jpg"]
    START_PICS = random.choice(START_PICS)
    USER_ID = message.from_user.id # GETTING MESSAGE FROM USER ID
    if USER_ID in AVAILABLE_USERS: # CHECKING USER IN DATABASE
        await message.reply_photo(photo=START_PICS, caption=f"""
**👋🏻 Hey {message.from_user.first_name}-san!**

__🎮 I'm your Hinata Game Bot, ready to be your loyal ally, just like Hinata is to Naruto! ❤️ Let's dive into exciting games and mysteries together! 👀 Ready for an epic adventure? 💫__

**🗯️ Check Below Buttons For More!**
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
            h = str(h)
            h = h.split("Telegram says: [420 FLOOD_WAIT_X] - A wait of ")[1]
            h = h.split(""" seconds is required (caused by "auth.ImportBotAuthorization")""")[0]
            h = int(h)
            raise Exception(f"Bot is in flood wait of {h} seconds, its required, bot automatically starts after {h} seconds")
            time.sleep(h+2)
            print("BOT STARTING AFTER FLOOD WAIT")
            bot.run()
        else:
            print(e)
