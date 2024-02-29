from HyperGames import GAME_DATABASE
from datetime import datetime, timedelta

db = GAME_DATABASE["Games_RO"]

async def check_claimed_user(user_id):
    user_data = await db.find_one({"user_id": user_id})
    return user_data

async def add_claimed_user(user_id):
    await db.update_one(
        {"user_id": user_id},
        {"$set": {"user_id": user_id, "last_claim_time": datetime.now()}},
        upsert=True
    )

async def update_last_claim_time(user_id):
    await db.update_one(
        {"user_id": user_id},
        {"$set": {"last_claim_time": datetime.now()}}
    )
