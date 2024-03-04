from HyperGames import *
from HyperGames.Database.games import *
from pyrogram import Client, filters
import os
import logging
import pyrogram
import random
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from HyperGames.Database.bank import *


LIST_BANKS_BUTTON = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("Telegram Bank", callback_data="TB_BANK"),
        InlineKeyboardButton("State Bank of Telegram", callback_data="SBT_BANK")
    ],
    [
        InlineKeyboardButton("HyperXbank™", callback_data="HB_BANK"),
        InlineKeyboardButton("YaxisBank", callback_data="Y_AXIS_BANK")
    ],
    [
        InlineKeyboardButton("CyberBank™", callback_data="CB_BANK")
    ]
]
