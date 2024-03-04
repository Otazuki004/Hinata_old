from HyperGames import HANDLER
from HyperGames.__main__ import bot
from pyrogram import filters
import asyncio
import os
from HyperGames.Database.games import *
from pyrogram import enums
import random
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@bot.on_message(filters.command(["delete_account", "deleteaccount"], prefixes=HANDLER))
async def delete_account(_, message):
    user_id = message.from_user.id
    if user_id not in await GET_AVAILABLE_USERS():
        return await message.reply("You don't have a account to delete.")
    await message.reply(
        text="Do you really want to delete account",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Confirm", callback_data=f"DELETE_AC_{user_id}")]
        ])
    )
