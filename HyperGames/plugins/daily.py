# © @KoraXD

from HyperGames import HANDLER
from HyperGames.__main__ import bot
from pyrogram import filters
from pyrogram.types import Message
from HyperGames.Database.games import ADD_COINS
from datetime import datetime, timedelta

claimed_users = {}

@bot.on_message(filters.command("daily") & filters.private)
async def daily_command(_, message: Message):
    user_id = message.from_user.id

    # To get bot's username
    try:
        bot_info = await bot.get_me()
        bot_username = bot_info.username
    except Exception as e:
        print(f"Error getting bot username: {e}")
        return await message.reply("**Error occurred say to owner!**")

    # To check user has bot's username in bio or not
    user = await bot.get_chat(user_id)
    user_bio = user.bio if user.bio else None
    if not user_bio or bot_username not in user_bio:
        return await message.reply(f"**🎉 Claim Daily Rewards! 🎁 Add @{bot_username} to Your Bio! 📲 Come Back in 2 Mins for Your Daily Treats! 🕒**")

# © @KoraXD

    if user_id in claimed_users:
        last_claim_time = claimed_users[user_id]
        current_time = datetime.now()
        time_difference = current_time - last_claim_time

        # Check if 24 hours completed or not
        if time_difference < timedelta(hours=24):
            time_left = timedelta(hours=24) - time_difference
            hours = time_left.seconds // 3600
            minutes = (time_left.seconds % 3600) // 60
            seconds = time_left.seconds % 60
            formatted_time_left = f"{hours:02}:{minutes:02}:{seconds:02}"
            return await message.reply(f"**🎁 Already Claimed! 🌟 Don't Forget to Keep @{bot_username} in Bio for Daily Rewards! ⚠ Come back after {formatted_time_left}.**")

    await ADD_COINS(user_id, 500)
    claimed_users[user_id] = datetime.now()
    claimed_message = "**🌟 Successfully Claimed! 🎉 Enjoy Your Daily Rewards of 500 Coins! 💰 Keep @{bot_username} in Bio or Lose Rewards! ⚠️ See You Tomorrow!**"
    await message.reply(claimed_message)

# © @KoraXD
