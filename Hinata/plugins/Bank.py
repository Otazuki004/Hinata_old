from Hinata import *
from Hinata.Database.main import *
from pyrogram import Client, filters
import os
import logging
import random
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
    global LIST_BANKS_BUTTON
    m = message
    user_id = message.from_user.id
    if user_id not in await GET_AVAILABLE_USERS():
        return await m.reply("You need a HyperGames account to use this command")
    elif await GET_BANK_SCORE(user_id) < 30:
        return await m.reply("You need atleast 30 bank score to create a bank account")
    elif await GET_COINS_FROM_USER(user_id) < 2000:
        return await m.reply("You need 2000 coins to create a bank account")
    elif await GET_USER_BANK_ACCOUNTS(user_id, get_as_count=True) >= 5:
        return await message.reply("You have already account in all bank")
    await message.reply(
        text="**Choose new the bank which you like**",
        reply_markup=LIST_BANKS_BUTTON
    )

@bot.on_message(filters.command("deposit", prefixes=HANDLER))
async def deposit_coins(_, message):
    m = message
    user_id = message.from_user.id
    if len(message.text.split()) <2:
        await message.reply("Enter the amount of coins to deposit it.")
        return
    coins = int(" ".join(message.command[1:]))
    DEPOSIT_STR = f"DEPOSIT_COINS\nUSER: {user_id}\nCOINS: {coins}\n"
    LIST_DEPOSIT_BUTTON = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Telegram bank", callback_data=f"{DEPOSIT_STR}TB"),
            InlineKeyboardButton("Federal bank", callback_data=f"{DEPOSIT_STR}FB")
        ],
        [
            InlineKeyboardButton("SBI", callback_data=f"{DEPOSIT_STR}SBI"),
            InlineKeyboardButton("Axis-Bank", callback_data=f"{DEPOSIT_STR}AXIS")
        ],
        [
            InlineKeyboardButton("CyberBank™", callback_data=f"{DEPOSIT_STR}CB")
        ]
    ])
    if user_id not in await GET_AVAILABLE_USERS():
        return await m.reply("You need a HyperGames account to use this command")
    elif await GET_USER_BANK_ACCOUNTS(user_id, get_as_count=True) == 0:
        return await m.reply("You need a bank account to use this command")
    elif await GET_COINS_FROM_USER(user_id) < coins:
        return await m.reply("You don't have enough coins to deposit.")
    elif coins <= 0:
        return await m.reply("Coins must be positive integer!.")
    else:
        await m.reply(
            text="Choose the bank below to deposit:",
            reply_markup=LIST_DEPOSIT_BUTTON
        )

@bot.on_message(filters.command("withdraw", prefixes=HANDLER))
async def WITHDRAW_COINS(_, message):
    m = message
    user_id = message.from_user.id
    if len(message.text.split()) <2:
        await message.reply("Enter the amount of coins to withdraw it.")
        return
    coins = int(" ".join(message.command[1:]))
    WITHDRAW_STR = f"WITHDRAW_COINS\nUSER: {user_id}\nCOINS: {coins}\n"
    LIST_WITHDRAW_BUTTON = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Telegram bank", callback_data=f"{WITHDRAW_STR}TB"),
            InlineKeyboardButton("Federal bank", callback_data=f"{WITHDRAW_STR}FB")
        ],
        [
            InlineKeyboardButton("SBI", callback_data=f"{WITHDRAW_STR}SBI"),
            InlineKeyboardButton("Axis-Bank", callback_data=f"{WITHDRAW_STR}AXIS")
        ],
        [
            InlineKeyboardButton("CyberBank™", callback_data=f"{WITHDRAW_STR}CB")
        ]
    ])
    if user_id not in await GET_AVAILABLE_USERS():
        return await m.reply("You need a HyperGames account to use this command")
    elif await GET_USER_BANK_ACCOUNTS(user_id, get_as_count=True) == 0:
        return await m.reply("You need a bank account to use this command")
    elif await GET_USER_COINS_FROM_BANK(user_id, total_coins=True) <= 0:
        return await message.reply("You don't coins in your all accounts!")
    elif coins <= 0:
        return await m.reply("Coins must be positive integer!.")
    else:
        await m.reply(
            text="Choose the bank below to withdraw:",
            reply_markup=LIST_WITHDRAW_BUTTON
    )
    
