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

async def GET_USER_BANK_ACCOUNTS(user_id, get_as_count=False):
    if get_as_count == False:
        Find = await db.find_one({"_id": 80556 + {user_id}})
        if not Find:
            return None
        else:
            value = Find.get("BANKS", [])
            return value
    else:
        Find = await db.find_one({"_id": 80556 + {user_id}})
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
    try:
        await db.update_one({"_id": 80556 + {user_id}}, {"$addToSet": {"BANKS": bank}}, upsert=True)
        await db.update_one({"_id": 80556 + {user_id}}, {"$inc": {"NUM_BANKS": 1}}, upsert=True)
    except Exception as e:
        print(f"Error adding new bank account to user {user_id}, {e}")
