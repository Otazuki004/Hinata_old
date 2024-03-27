from Hinata import *
from Hinata.__main__ import bot
from pyrogram import filters
import asyncio
import os
from Hinata.Database.main import *
from pyrogram import enums
import random
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from restart import restart_program

BUTTONS = InlineKeyboardMarkup([[InlineKeyboardButton("» 𝗛ʏᴘᴇʀ 𝗦ᴘᴇᴇᴅ™", url="https://t.me/Hyper_Speed0")]])


async def choice_generator(user_one: int, user_one_lvl: int, user_two: int, user_two_lvl: int):
    if user_one_lvl > user_two_lvl:
        if user_one_lvl < 3:
            chance = 0.5
        elif user_one_lvl < 7:
            chance = 0.33
        elif user_one_lvl < 16:
            chance = 0.4
        elif user_one_lvl < 25:
            chance = 0.43
        elif user_one_lvl < 38:
            chance = 0.47
        elif user_one_lvl < 50:
            chance = 0.45
        elif user_one_lvl < 75:
            chance = 0.53
        elif user_one_lvl < 100:
            chance = 0.5
        else:
            chance = 0.65
        random_choice = random.random()
        return user_two if random_choice < chance else user_one
    else:
        user_one_lvl = user_two_lvl 
        user_two_lvl = user_one_lvl
        if user_one_lvl < 3:
            chance = 0.5
        elif user_one_lvl < 7:
            chance = 0.33
        elif user_one_lvl < 16:
            chance = 0.4
        elif user_one_lvl < 25:
            chance = 0.43
        elif user_one_lvl < 38:
            chance = 0.47
        elif user_one_lvl < 50:
            chance = 0.45
        elif user_one_lvl < 75:
            chance = 0.53
        elif user_one_lvl < 100:
            chance = 0.5
        else:
            chance = 0.90
        random_choice = random.random()
        return user_one if random_choice < chance else user_two


@bot.on_message(filters.command("profile", prefixes=HANDLER) & floodfilter)
async def get_profile(_, message):
    list_users = await GET_AVAILABLE_USERS()
    user_id = message.from_user.id
    if message.reply_to_message:
        if message.chat.type == enums.ChatType.PRIVATE:
            user_id = message.from_user.id
        elif message.reply_to_message.from_user.is_bot:
            return await message.reply("You can't get profile to bots.")
        if message.reply_to_message.from_user.id in list_users:
            user_id = message.reply_to_message.from_user.id
        else:
            return await message.reply("Sorry, the user you replied to doesn't have an account. You need a Hyper Games account to use this command.")
    if user_id in list_users:
        user_coins = await GET_COINS_FROM_USER(user_id)
        pfp = await GET_PROFILE_PIC(user_id)
        exp = await GET_EXP(user_id)
        name = await GET_USER_NAME(user_id)
        level = await GET_LEVEL(user_id)
        bank_score = await GET_BANK_SCORE(user_id)
        bank_accounts = await GET_USER_BANK_ACCOUNTS(user_id, get_as_count=True)
        total_coins_bank = await GET_USER_COINS_FROM_BANK(user_id, total_coins=True)
        if pfp == None:
            await message.reply_photo("https://telegra.ph/file/a359e56250bd60eb192ff.jpg", caption=f"""
**•> GAMER INFO**
▰▱▰▱▰▱▰▱▰▱▰▱▰

**➤ Name:** {name}
**➤ ID:** `{user_id}`
**➤ Coins:** `{user_coins}`
**➤ Level:** `{level}`
**➤ Experience:** `{exp}`
**➤ Weapons:** `None`
**➤ Tools:** `None`
**➤ Relationship points:** `None`
**➤ Characters:** `None`
**➤ Bank accounts:** `{bank_accounts}`
**➤ Bank score:** `{bank_score}/100`
**➤ Bank Balance:** `{total_coins_bank}`

**•> Powered by @Hyper_Speed0™**
""", reply_markup=BUTTONS)
        else:
            await message.reply_photo(pfp, caption=f"""
**•> GAMER INFO**
▰▱▰▱▰▱▰▱▰▱▰▱▰

**➤ Name:** {name}
**➤ ID:** `{user_id}`
**➤ Coins:** `{user_coins}`
**➤ Level:** `{level}`
**➤ Experience:** `{exp}`
**➤ Weapons:** `None`
**➤ Tools:** `None`
**➤ Relationship points:** `None`
**➤ Characters:** `None`
**➤ Bank accounts:** `{bank_accounts}`
**➤ Bank score:** `{bank_score}/100`
**➤ Bank Balance:** `{total_coins_bank}`

**•> Powered by @Hyper_Speed0™**
""", reply_markup=BUTTONS)
    else:
        await message.reply("You don't have a Hyper Games account, Create a Account by /start")
        return
        
@bot.on_message(filters.command(["send", "sent", "transfer"], prefixes=HANDLER) & floodfilter)
async def send_coins(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Please specify the amount of coins to send.")
    if not message.reply_to_message:
        return await message.reply("You need to reply to a user to send coins.")
    if message.reply_to_message.from_user.id == message.from_user.id:
        return await message.reply("You can't send coins to yourself.")
    if message.reply_to_message.from_user.is_bot:
        return await message.reply("You can't send coins to bots")
    coins = " ".join(message.command[1:])
    int_coins = int(coins)
    reply_usr = message.reply_to_message.from_user.id
    user_id = message.from_user.id
    send_status = await SEND_COINS(user_id, reply_usr, int_coins)
    if send_status == "FROM_USER_NOT_FOUND":
        return await message.reply("You need an account to use this command.")
    elif send_status == "TO_USER_NOT_FOUND":
        return await message.reply("The user you replied to doesn't have an account. Accounts are required for this command.")
    elif send_status == "NOT_ENOUGH_COINS":
        return await message.reply("You don't have enough coins to send.")
    elif send_status == "NOT_POSITIVE_NUMBER":
        return await message.reply("Please enter a positive integer.")
    elif send_status == "SUCCESS":
        return await message.reply(f"Successfully sent `{int_coins}` coins.")
    elif send_status.startswith("ERROR"):
        return await message.reply(send_status)

@bot.on_message(filters.command("bet", prefixes=HANDLER) & floodfilter)
async def bet_coins(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Please enter the amount of coins to bet.")
    coins = " ".join(message.command[1:])
    int_coins = int(coins)
    user_id = message.from_user.id
    bet_status = await BET_COINS(user_id, int_coins)
    if bet_status == "USER_NOT_FOUND":
        return await message.reply("You need an account to use this command.")
    elif bet_status == "NOT_ENOUGH_COINS":
        return await message.reply("You don't have enough coins to bet.")
    elif bet_status == "NOT_POSTIVE_NUMBER":
        return await message.reply("Please enter a positive integer.")
    elif bet_status.startswith("ERROR"):
        return await message.reply(bet_status)
    elif bet_status == "LOSE":
        return await message.reply(f"Sorry, you lost {int_coins} coins.")
    elif bet_status == "PRO":
        return await message.reply(f"Congratulations! You won {int_coins*2} coins with a pro bet!")
    elif bet_status.startswith("BLOCKED"):
        h = bet_status.split("BLOCKED_")[1]
        return await message.reply(f"You have blocked using bet for 10 minutes, time you blocked: {h}")
    else:
        return await message.reply(f"You won {bet_status} coins!")

@bot.on_message(filters.command(["setpfp", "setprofile"], prefixes=HANDLER))
async def set_profile_photo(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Please provide a valid image link to set as your profile picture.")
    image_link = " ".join(message.command[1:])
    if image_link.startswith("https://"):
        status = await SET_PROFILE_PIC(message.from_user.id, image_link)
        if status == "USER_NOT_FOUND":
            return await message.reply("You need an account to use this command.")
        elif status == "NOT_ENOUGH_COINS":
            return await message.reply("You need at least 1000 coins to use this command.")
        elif status == "SUCCESS":
            return await message.reply("Success! Your profile picture has been updated.")
    else:
        return await message.reply("Please provide a valid image link starting with 'https://'.")
        
@bot.on_message(filters.command(["setname", "setnewname"], prefixes=HANDLER) & floodfilter)
async def set_name(_, message):
    user_id = message.from_user.id
    TASK_COMPLETED = {}
    TASK_COMPLETED[user_id] = False
    if TASK_COMPLETED[user_id] == True:
        TASK_COMPLETED[user_id] = False
    if user_id not in await GET_AVAILABLE_USERS():
        return await message.reply("You need a account to use this command")
    await message.reply_text("Please enter your new name.")
    @bot.on_message(filters.user(user_id) & filters.reply)
    async def setting_name(_, message):
        global TASK_COMPLETED
        if message.from_user.id == user_id and not TASK_COMPLETED[user_id] == True:
            new_name = message.text
            if len(new_name) >= 20:
                await message.reply("Name must be below 20 characters!")
                TASK_COMPLETED[user_id] == True
                return 
            status = await SET_USER_NAME(message.from_user.id, new_name)
            if status == "NOT_ENOUGH_COINS":
                await message.reply("You need at least 1999 coins to use this command.")
                TASK_COMPLETED[user_id] = True
            elif status == "SUCCESS":
                await message.reply("Success! Your profile name has been updated.")
                TASK_COMPLETED[user_id] = True
                return 

@bot.on_message(filters.command("fight", prefixes=HANDLER) & floodfilter)
async def fight(_, message):
    if message.reply_to_message:
        if message.reply_to_message.from_user.id == message.from_user.id:
            return await message.reply("You can't fight yourself!")
        elif message.chat.type == enums.ChatType.PRIVATE:
            return await message.reply("This command only works on Groups")
        elif message.reply_to_message.from_user.is_bot:
            return await message.reply("You can't fight to bots.")
        list_users = await GET_AVAILABLE_USERS()
        reply_user = message.reply_to_message.from_user.id
        user_id = message.from_user.id
        coins_reply_user = await GET_COINS_FROM_USER(reply_user)
        coins_user = await GET_COINS_FROM_USER(user_id)
        if user_id not in list_users:
            return await message.reply("You need an account to use this command.")
        elif reply_user not in list_users:
            return await message.reply("The user you replied to doesn't have an account. Accounts are required for this command.")
        elif coins_reply_user < 500:
            return await message.reply("The user you replied to needs at least 500 coins to fight.")
        elif coins_user < 500:
            return await message.reply("You need at least 500 coins to fight.")
        fight_message = await message.reply("The fight has begun!")
        await asyncio.sleep(1)
        await fight_message.edit("•")
        await asyncio.sleep(1)
        await fight_message.edit("••")
        await asyncio.sleep(0.6)
        await fight_message.edit("•••")
        await asyncio.sleep(0.6)
        fr_first_name = message.from_user.first_name
        rp_first_name = message.reply_to_message.from_user.first_name
        fr_user_lvl = await GET_LEVEL(user_id)
        rp_user_lvl = await GET_LEVEL(reply_user)
        random_choice = await choice_generator(user_id, fr_user_lvl, reply_user, rp_user_lvl)
        if random_choice == user_id:
            await UPDATE_EXP(user_id, 2)
            send_coins_status = await SEND_COINS(reply_user, user_id, 500)
            if send_coins_status == "SUCCESS":
                return await fight_message.edit(f"The fight was intense, but the winner is {fr_first_name}! They received 500 coins from {rp_first_name}.")
        else:
            await UPDATE_EXP(reply_user, 2)
            send_coins_status = await SEND_COINS(user_id, reply_user, 500)
            if send_coins_status == "SUCCESS":
                return await fight_message.edit(f"The fight was intense, but the winner is {rp_first_name}! They received 500 coins from {fr_first_name}.")
    else:
        return await message.reply("Please reply to a user to initiate a fight.")
