from HyperGames import GAME_DATABASE
import asyncio
import random
from HyperGames.Database.games import *

db = GAME_DATABASE["Games_RO"]

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