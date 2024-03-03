from HyperGames import HANDLER
from HyperGames.__main__ import bot
from pyrogram import filters
import asyncio
import os
from HyperGames.Database.games import *
from pyrogram import enums
import random
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

CONFIRM_BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton("Confirm", callback_data="DELETE_AC")]
])

@bot.on_message(filters.command(["delete_account", "deleteaccount"], prefixes=HANDLER))
async def delete_account(_, message):
    await message.reply(
        text="Do you really want to delete account",
        reply_markup=CONFIRM_BUTTON
    )
