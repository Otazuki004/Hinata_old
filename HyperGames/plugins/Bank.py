from HyperGames import *
from HyperGames.Database.games import *
from pyrogram import Client, filters
import os
import logging
import pyrogram
import random
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


LIST_BANKS_BUTTON = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("Telegram bank", callback_data="TB_BANK"),
        InlineKeyboardButton("Federal bank", callback_data="FB_BANK")
    ],
    [
        InlineKeyboardButton("SBI", callback_data="SBI_BANK"),
        InlineKeyboardButton("Axis-Bank", callback_data="AXIS_BANK")
    ],
    [
        InlineKeyboardButton("CyberBank™", callback_data="CB_BANK")
    ]
])

@bot.on_message(filters.command("cb", prefixes=HANDLER))
async def create_bank_account(_, message):
    m = message
    user_id = message.from_user.id
    if user_id not in await GET_AVAILABLE_USERS():
        return await m.reply("You need a HyperGames account to use this command")
    elif await GET_BANK_SCORE(user_id) < 30:
        return await m.reply("You need atleast 30 bank score to create a bank account")
    elif await GET_COINS_FROM_USER(user_id) < 2000:
        return await m.reply("You need 2000 coins to create a bank account")
    await message.reply(
        text="**Choose new the bank which you like**",
        reply_markup=LIST_BANKS_BUTTON
    )
