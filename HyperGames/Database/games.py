from HyperGames import GAME_DATABASE
import asyncio
import random

db = GAME_DATABASE["Games_R"]

async def GET_AVAILABLE_USERS():
    Find = await db.find_one({"_id": 1})
    if not Find:
        return []
    else:
        value = Find.get("USERS", [])
        return value

async def ADD_NEW_USER(user_id):
    doc = {"_id": 4444 + user_id, "NAME": "Steve_HS"}
    await db.insert_one(doc)
    await db.update_one({"_id": 1}, {"$addToSet": {"USERS": user_id}}, upsert=True)

async def GET_COINS_FROM_USER(user_id: int):
    document_id = f"user_{user_id}"
    try:
        user_data = await db.find_one({"_id": document_id})
        if user_data:
            return user_data.get("coins", 0)
        else:
            return 0  # Handle case where user document is not found
    except Exception as e:
        # Handle exceptions
        print(f"Error getting coins for user {user_id}: {e}")
        return 0

async def ADD_COINS(user_id: int, coins: int):
    document_id = f"user_{user_id}"
    try:
        await db.update_one(
            {"_id": document_id},
            {"$inc": {"coins": coins}},
            upsert=True
        )
    except Exception as e:
        # Handle exceptions
        print(f"Error updating coins for user {user_id}: {e}")

async def REMOVE_USER(user_id):
    document_id = f"user_{user_id}"
    await db.delete_one({"_id": document_id})
    await db.update_one({"_id": 1}, {"$pull": {"USERS": user_id}})
    try:
        await db.delete_one({"_id": 888 + user_id})
    except Exception as e:
        print("Its normal error i guess", e)
    try:
        await db.delete_one({"_id": 4444 + user_id})
    except Exception as e:
        print("Its normal error i guess", e)
    
    
async def SEND_COINS(from_user: int, to_user: int, coins: int):
    USERS_ACC = await GET_AVAILABLE_USERS()
    if from_user not in USERS_ACC:
        return "FROM_USER_NOT_FOUND"
    elif to_user not in USERS_ACC:
        return "TO_USER_NOT_FOUND"
    COINS_FR_USR = await GET_COINS_FROM_USER(from_user)
    if coins > COINS_FR_USR:
        return "NOT_ENOUGH_COINS"
    elif coins <= 0:
        return "NOT_POSTIVE_NUMBER"
    elif coins <= COINS_FR_USR:
        try:
            await ADD_COINS(from_user, -coins)
            await ADD_COINS(to_user, coins)
            return "SUCCESS"
        except Exception as e:
            ERROR_RETURN_STR = f"ERROR, {e}"
            return ERROR_RETURN_STR

async def SET_PROFILE_PIC(user_id: int, image: str):
    USERS_ACC = await GET_AVAILABLE_USERS()
    if user_id not in USERS_ACC:
        return "USER_NOT_FOUND"
    COINS_USR = await GET_COINS_FROM_USER(user_id)
    if COINS_USR >= 1000:
        await ADD_COINS(user_id, -1000)
        doc = {"_id": 888 + user_id, "IMAGE": image}
        try:
            await db.insert_one(doc)
        except Exception:
            await db.update_one({"_id": 888 + user_id}, {"$set": {"IMAGE": image}})
        return "SUCCESS"
    else:
        return "NOT_ENOUGH_COINS"

async def GET_PROFILE_PIC(user_id: int):
    Find = await db.find_one({"_id": 888 + user_id})
    if not Find:
        return None
    else:
        value = Find["IMAGE"]
        return value

async def SET_USER_NAME(user_id: int, name: str):
    USERS_ACC = await GET_AVAILABLE_USERS()
    if user_id not in USERS_ACC:
        return "USER_NOT_FOUND"
    COINS_USR = await GET_COINS_FROM_USER(user_id)
    if COINS_USR >= 1999:
        await ADD_COINS(user_id, -1999)
        doc = {"_id": 4444 + user_id, "NAME": name}
        try:
            await db.insert_one(doc)
        except Exception:
            await db.update_one({"_id": 4444 + user_id}, {"$set": {"NAME": name}})
        return "SUCCESS"
    else:
        return "NOT_ENOUGH_COINS"


async def GET_USER_NAME(user_id: int):
    Find = await db.find_one({"_id": 4444 + user_id})
    if not Find:
        return None
    else:
        value = Find["NAME"]
        return value

async def ADD_LEVEL(user_id: int, level: int):
    document_id = f"user_{user_id}"
    try:
        await db.update_one(
            {"_id": document_id},
            {"$set": {"LVL": level}},
            upsert=True
        )
    except Exception as e:
        print(f"Error adding level for user {user_id}: {e}")
                

async def UPDATE_EXP(user_id: int, exp: int):
    document_id = f"user_{user_id}"
    try:
        await db.update_one(
            {"_id": document_id},
            {"$inc": {"EXP": exp}},
            upsert=True
        )
    except Exception as e:
        print(f"Error updating exp for user {user_id}: {e}")
        
async def GET_EXP(user_id: int):
    document_id = f"user_{user_id}"
    try:
        user_data = await db.find_one({"_id": document_id})
        if user_data:
            return user_data.get("EXP", 0)
        else:
            return 0 
    except Exception as e:
        print(f"Error getting exp for user {user_id}: {e}")
        return 0
        

async def GET_LEVEL(user_id: int):
    document_id = f"user_{user_id}"
    try:
        user_data = await db.find_one({"_id": document_id})
        if user_data:
            EXP = await GET_EXP(user_id)
            LEVEL = user_data.get("LVL", 0)
            LEVEL_CH = EXP // 250
            if LEVEL_CH == LEVEL:
                return user_data.get("LVL", 0)
            else:
                await ADD_LEVEL(user_id, LEVEL_CH)
                return int(LEVEL_CH)
        else:
            return 0 
    except Exception as e:
        print(f"Error getting level for user {user_id}: {e}")
        return 0
        
    
async def BET_COINS(user_id: int, coins: int):
    USERS_ACC = await GET_AVAILABLE_USERS()
    LEVEL = await GET_LEVEL(user_id)
    if user_id not in USERS_ACC:
        return "USER_NOT_FOUND"
    COINS_USR = await GET_COINS_FROM_USER(user_id)
    if coins > COINS_USR:
        return "NOT_ENOUGH_COINS"
    elif coins <= 0:
        return "NOT_POSTIVE_NUMBER"
    elif coins <= COINS_USR:
        try:
            if LEVEL < 1:
                LUCK_LIST = ['YES', 'NO', 'YES']
            elif LEVEL < 3:
                LUCK_LIST = ['YES', 'NO']
            elif LEVEL < 5:
                LUCK_LIST = ['YES', 'NO', 'NO']
            elif LEVEL < 7:
                LUCK_LIST = ['YES', 'NO', 'NO', 'NO', 'PRO']
            elif LEVEL < 15:
                LUCK_LIST = ['YES', 'NO', 'NO', 'NO', 'PRO', 'PRO']
            elif LEVEL < 30:
                LUCK_LIST = ['YES', 'NO', 'NO', 'NO', 'NO', 'PRO', 'PRO']
            elif LEVEL < 60:
                LUCK_LIST = ['YES', 'NO', 'YES', 'NO', 'NO', 'NO', 'NO', 'PRO', 'PRO']
            elif LEVEL < 100:
                LUCK_LIST = ['YES', 'NO', 'YES', 'NO', 'NO', 'NO', 'NO', 'NO', 'NO', 'PRO', 'PRO']
            elif LEVEL > 100:
                LUCK_LIST = ['YES', 'NO', 'YES', 'NO', 'NO', 'NO', 'NO', 'PRO', 'PRO', 'PRO', 'PRO', 'PRO', 'NO']
            PER_50 = (coins / 100) * 50
            PER_50 = int(PER_50)
            RANDOM_COINS = random.randint(PER_50, coins)
            GET_LUCK = random.choice(LUCK_LIST)
            if RANDOM_COINS <= 0:
                RANDOM_COINS = 1
            if GET_LUCK == 'YES':
                await ADD_COINS(user_id, RANDOM_COINS)
                RANDOM_COINS = str(RANDOM_COINS)
                await UPDATE_EXP(user_id, 1)
                return RANDOM_COINS
            elif GET_LUCK == 'NO':
                mins_coins = f"-{coins}"
                mins_coins = int(mins_coins)
                await ADD_COINS(user_id, mins_coins)
                return "LOSE"
            elif GET_LUCK == 'PRO':
                await UPDATE_EXP(user_id, 3)
                coins_2x = coins*2
                await ADD_COINS(user_id, coins_2x)
                return "PRO"
        except Exception as e:
            string = f"ERROR, {e}"
            return string

"""async def TRANSFER_ACCOUNT(old_account_id: int, to_user_id: int):
    USERS_LIST = await GET_AVAILABLE_USERS()
    if old_account_id not in USERS_LIST:
        return "USER_NOT_FOUND"
    elif to_user_id in USERS_LIST:
        return "NEW_ID_ALREADY_EXITS"
    document_id = f"user_{old_account_id}"
    """ # i will complete soon
    
