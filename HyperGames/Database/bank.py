from HyperGames import GAME_DATABASE
import asyncio
import random
from HyperGames.Database.games import *

db = GAME_DATABASE["Games_RO"]
AVAILABLE_BANKS = ['TB', 'SBT', 'HB', 'Y_AXIS_BANK', 'CB']
# The meanings of bank above Telegram bank, state Bank of telegram, Hyper bank, Y_AXIS_BANK, Cyber Bank

async def GET_BANK_SCORE(user_id: int):
    if user_id not in await GET_AVAILABLE_USERS():
        return "USER_NOT_FOUND"
    document_id = f"user_{user_id}"
    try:
        user_data = await db.find_one({"_id": document_id})
        if user_data:
            return user_data.get("SCORE", 0)
        else:
            return 0
    except Exception as e:
        return print(f"Error getting bank score for user {user_id}: {e}")

async def ADD_BANK_SCORE(user_id: int, score: int):
    if user_id not in await GET_AVAILABLE_USERS():
        return "USER_NOT_FOUND"
    elif GET_BANK_SCORE(user_id) >= 100:
        return "BANK_SCORE_ALREADY_MAX"
    document_id = f"user_{user_id}"
    try:
        await db.update_one(
            {"_id": document_id},
            {"$inc": {"SCORE": score}},
            upsert=True
        )
    except Exception as e:
        return print(f"Error updating bank score for user {user_id}: {e}")

async def GET_USER_BANK_ACCOUNTS(user_id: int, get_as_count=False):
    if get_as_count == False:
        Find = await db.find_one({"_id": 80556+user_id})
        if not Find:
            return None
        else:
            value = Find.get("BANKS", [])
            return value
    else:
        Find = await db.find_one({"_id": 80556+user_id})
        if not Find:
            return 0
        else:
            value = Find.get("NUM_BANKS", 0)
            return value
        
async def CREATE_USER_BANK_ACCOUNT(user_id, bank):
    if user_id not in await GET_AVAILABLE_USERS():
        return "USER_NOT_FOUND"
    elif await GET_BANK_SCORE(user_id) < 30:
        return "NOT_ENOUGH_BANK_SCORE"
    elif bank not in AVAILABLE_BANKS:
        return "BANK_NOT_FOUND"
    elif await GET_USER_BANK_ACCOUNTS(user_id) == bank:
        return "USER_ALREADY_HAVE_ACCOUNT_IN_THIS_BANK"
    try:
        await db.update_one({"_id": 80556+{user_id}}, {"$addToSet": {"BANKS": bank}}, upsert=True)
        await db.update_one({"_id": 80556+{user_id}}, {"$inc": {"NUM_BANKS": 1}}, upsert=True)
    except Exception as e:
        print(f"Error adding new bank account to user {user_id}, {e}")

async def GET_USER_COINS_FROM_BANK(user_id: int, bank=None, total_coins=False):
    if total_coins == False:
        if bank == None:
            raise Exception "required 2 required argument 'user_id' 'bank' only its required when total_coins in False"
            return
        Find = await db.find_one({"_id": 97280+user_id})
        if not Find:
            return 0
        else:
            value = Find.get(bank, 0)
            return value
    else:
        Find = await db.find_one({"_id": 97789+user_id})
        if not Find:
            return 0
        else:
            value = Find.get("TOTAL_COINS", 0)
            return value
    
async def DEPOSIT_COINS(user_id: int, coins: int, bank: str):
    if user_id not in await GET_AVAILABLE_USERS():
        return "USER_NOT_FOUND"
    elif bank not in AVAILABLE_BANKS:
        return "BANK_NOT_FOUND"
    elif await GET_COINS_FROM_USER(user_id) < coins:
        return "NOT_ENOUGH_COINS"
    elif bank not in await GET_USER_BANK_ACCOUNTS(user_id):
        return "USER_HAVE_NO_ACCOUNT_IN_THAT_BANK"
    try:
        coin_minus = f"-{coins}"
        coin_minus = int(coin_minus)
        await ADD_COINS(user_id, coin_minus)
        await db.update_one({"_id": 97280+{user_id}}, {"$inc": {f"{bank}": coins}}, upsert=True)
        await db.update_one({"_id": 97789+{user_id}}, {"$inc": {f"TOTAL_COINS": coins}}, upsert=True)
        return "SUCCESS"
    except Exception as e:
        print(f"Error while depositing coins to user {user_id}: {e}")
        return f"ERROR, {e}"

async def WITHDRAW_COINS_FROM_BANK(user_id: int, coins: int, bank: int):
    
