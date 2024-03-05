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
        InlineKeyboardButton("Telegram Bank", callback_data="TB_BANK"),
        InlineKeyboardButton("SBT BANK", callback_data="SBT_BANK")
    ],
    [
        InlineKeyboardButton("Hyper-Bank™", callback_data="HB_BANK"),
        InlineKeyboardButton("YaxisBank", callback_data="Y_AXIS_BANK")
    ],
    [
        InlineKeyboardButton("CyberBank™", callback_data="CB_BANK")
    ]
])

@bot.on_message(filters.command("cb", prefixes=HANDLER))
async def create_bank_account(_, message):
    await message.reply(
        text="Under development",
        reply_markup=LIST_BANKS_BUTTON
    )
