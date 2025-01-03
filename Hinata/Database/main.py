from Hinata import GAME_DATABASE
import asyncio
import random
from datetime import datetime 

db = GAME_DATABASE["Games_RO"]
AVAILABLE_BANKS = ['TB', 'FB', 'SBI', 'AXIS', 'CB']

# GETTING LIST USERS
async def GET_AVAILABLE_USERS():
    Find = await db.find_one({"_id": 1})
    if not Find:
        return []
    else:
        value = Find.get("USERS", [])
        return value
# ADDED NEW USER 
async def ADD_NEW_USER(user_id):
    if user_id in await GET_AVAILABLE_USERS():
        return "USER_ALREADY_EXITS"
    doc = {"_id": 4444 + user_id, "NAME": "Steve_HS"}
    await db.insert_one(doc)
    await db.update_one({"_id": 1}, {"$addToSet": {"USERS": user_id}}, upsert=True)

# GETTING COINS FROM THE USER
async def GET_COINS_FROM_USER(user_id: int):
    document_id = f"user_{user_id}"
    try:
        user_data = await db.find_one({"_id": document_id})
        if user_data:
            return user_data.get("coins", 0)
        else:
            return 0
    except Exception as e:
        raise Exception(f"Error getting coins for user {user_id}: {e}")
        return 0
# UPDATE THE COINS FROM USER
async def UPDATE_COINS(user_id: int, coins: int):
    if user_id not in await GET_AVAILABLE_USERS():
        return "USER_NOT_FOUND_CREATE_ACCOUNT_AND_TRY"
    document_id = f"user_{user_id}"
    try:
        await db.update_one(
            {"_id": document_id},
            {"$inc": {"coins": coins}},
            upsert=True
        )
    except Exception as e:
        raise Exception(f"Error updating coins for user {user_id}: {e}")

# REMOVEING THE USER
async def REMOVE_USER(user_id):
    if user_id not in await GET_AVAILABLE_USERS():
        return "USER_NOT_FOUND"
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
    try:
        await db.delete_one({"_id": 80556+user_id})
    except Exception as e:
        print("Its normal error i guess", e)
    try:
        await db.delete_one({"_id": 97280+user_id})
    except Exception as e:
        print("Its normal error i guess", e)
    try:
        await db.delete_one({"_id": 97789+user_id})
    except Exception as e:
        print("Its normal error i guess", e)
    
# SENDING COINS TO ANOTHER USER
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
            await UPDATE_COINS(from_user, -coins)
            await UPDATE_COINS(to_user, coins)
            return "SUCCESS"
        except Exception as e:
            ERROR_RETURN_STR = f"ERROR, {e}"
            return ERROR_RETURN_STR

# SETTING PROFILE PIC TO USER
async def SET_PROFILE_PIC(user_id: int, image: str):
    USERS_ACC = await GET_AVAILABLE_USERS()
    if user_id not in USERS_ACC:
        return "USER_NOT_FOUND"
    COINS_USR = await GET_COINS_FROM_USER(user_id)
    if COINS_USR >= 1000:
        await UPDATE_COINS(user_id, -1000)
        doc = {"_id": 888 + user_id, "IMAGE": image}
        try:
            await db.insert_one(doc)
        except Exception:
            await db.update_one({"_id": 888 + user_id}, {"$set": {"IMAGE": image}})
        return "SUCCESS"
    else:
        return "NOT_ENOUGH_COINS"

# GETTING PROFILE PIC TO USER
async def GET_PROFILE_PIC(user_id: int):
    Find = await db.find_one({"_id": 888 + user_id})
    if not Find:
        return None
    else:
        value = Find["IMAGE"]
        return value

# SETING USER'S NAME
async def SET_USER_NAME(user_id: int, name: str):
    USERS_ACC = await GET_AVAILABLE_USERS()
    if user_id not in USERS_ACC:
        return "USER_NOT_FOUND"
    COINS_USR = await GET_COINS_FROM_USER(user_id)
    if COINS_USR >= 1999:
        await UPDATE_COINS(user_id, -1999)
        doc = {"_id": 4444 + user_id, "NAME": name}
        try:
            await db.insert_one(doc)
        except Exception:
            await db.update_one({"_id": 4444 + user_id}, {"$set": {"NAME": name}})
        return "SUCCESS"
    else:
        return "NOT_ENOUGH_COINS"

# GETTING USER'S NAME
async def GET_USER_NAME(user_id: int):
    Find = await db.find_one({"_id": 4444 + user_id})
    if not Find:
        return None
    else:
        value = Find["NAME"]
        return value

# ADDING LEVEL
async def ADD_LEVEL(user_id: int, level: int):
    document_id = f"user_{user_id}"
    try:
        await db.update_one(
            {"_id": document_id},
            {"$set": {"LVL": level}},
            upsert=True
        )
    except Exception as e:
        raise Exception(f"Error adding level for user {user_id}: {e}")

# GETTING BANK SCORE 
async def GET_BANK_SCORE(user_id: int):
    USRS = await GET_AVAILABLE_USERS()
    if user_id not in USRS:
        return "USER_NOT_FOUND"
    document_id = f"user_{user_id}"
    try:
        user_data = await db.find_one({"_id": document_id})
        if user_data:
            SCORE = user_data.get("SCORE", 0)
            if SCORE >= 100:
                return 100
            else:
                return SCORE
        else:
            return 0
    except Exception as e:
        return print(f"Error getting bank score for user {user_id}: {e}")

# ADD BANK SCORE
async def ADD_BANK_SCORE(user_id: int, score: int):
    USRS = await GET_AVAILABLE_USERS()
    if user_id not in USRS:
        return "USER_NOT_FOUND"
    elif await GET_BANK_SCORE(user_id) >= 100:
        return
    document_id = f"user_{user_id}"
    try:
        await db.update_one(
            {"_id": document_id},
            {"$inc": {"SCORE": score}},
            upsert=True
        )
    except Exception as e:
        return print(f"Error updating bank score for user {user_id}: {e}")

# GET USER BANK ACCOUNTS
async def GET_USER_BANK_ACCOUNTS(user_id: int, get_as_count=False):
    if get_as_count == False:
        Find = await db.find_one({"_id": 80556+user_id})
        if not Find:
            return []
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

# CREATE NEW BANK ACCOUNT 
async def CREATE_USER_BANK_ACCOUNT(user_id, bank):
    USRS = await GET_AVAILABLE_USERS()
    if user_id not in USRS:
        return "USER_NOT_FOUND"
    elif await GET_BANK_SCORE(user_id) < 30:
        return "NOT_ENOUGH_BANK_SCORE"
    elif bank not in AVAILABLE_BANKS:
        return "BANK_NOT_FOUND"
    elif bank in await GET_USER_BANK_ACCOUNTS(user_id, get_as_count=False):
        return "USER_ALREADY_HAVE_ACCOUNT_IN_THIS_BANK"
    elif await GET_COINS_FROM_USER(user_id) < 2000:
        return "LOW_COINS"
    try:
        await db.update_one({"_id": 80556+user_id}, {"$addToSet": {"BANKS": bank}}, upsert=True)
        await db.update_one({"_id": 80556+user_id}, {"$inc": {"NUM_BANKS": 1}}, upsert=True)
        await UPDATE_COINS(user_id, -2000)
        return "SUCCESS"
    except Exception as e:
        print(f"Error adding new bank account to user {user_id}, {e}")
        return f"**Error:** {e}"

# GET COINS FROM BANK
async def GET_USER_COINS_FROM_BANK(user_id: int, bank=None, total_coins=False):
    if total_coins == False:
        if bank == None:
            raise Exception("required 2 arguments 'user_id' and 'bank' for getting user coins in specific bank")
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

# DEPOSIT COINS
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
        await UPDATE_COINS(user_id, coin_minus)
        await db.update_one({"_id": 97280+user_id}, {"$inc": {f"{bank}": coins}}, upsert=True)
        await db.update_one({"_id": 97789+user_id}, {"$inc": {f"TOTAL_COINS": coins}}, upsert=True)
        return "SUCCESS"
    except Exception as e:
        print(f"Error while depositing coins to user {user_id}: {e}")
        return f"ERROR, {e}"

# WITHDRA COINS 
async def WITHDRAW_COINS_FROM_BANK(user_id: int, coins: int, bank: int):
    if user_id not in await GET_AVAILABLE_USERS():
        return "USER_NOT_FOUND"
    elif bank not in AVAILABLE_BANKS:
        return "BANK_NOT_FOUND"
    elif bank not in await GET_USER_BANK_ACCOUNTS(user_id):
        return "USER_HAVE_NO_ACCOUNT_IN_THAT_BANK"
    elif not await GET_USER_COINS_FROM_BANK(user_id, bank) >= coins:
        return "NOT_ENOUGH_COINS_IN_BANK"
    try:
        coin_minus = f"-{coins}"
        coin_minus = int(coin_minus)
        await db.update_one({"_id": 97280+user_id}, {"$inc": {f"{bank}": coin_minus}}, upsert=True)
        await db.update_one({"_id": 97789+user_id}, {"$inc": {f"TOTAL_COINS": coin_minus}}, upsert=True)
        await ADD_COINS(user_id, coins)
        return "SUCCESS"
    except Exception as e:
        print(f"Error while withdrawing coins to user {user_id}: {e}")
        return f"ERROR, {e}"

async def UPDATE_EXP(user_id: int, exp: int):
    if user_id not in await GET_AVAILABLE_USERS():
        return "USER_NOT_FOUND"
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
            BANK_SCORE = await GET_BANK_SCORE(user_id)
            BANK_CH = EXP // 12
            if not BANK_SCORE == BANK_CH:
                await ADD_BANK_SCORE(user_id, BANK_CH)
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
            elif LEVEL < 29999:
                LUCK_LIST = ['YES', 'NO', 'YES', 'NO', 'NO', 'NO', 'NO', 'PRO', 'PRO', 'PRO', 'PRO', 'PRO', 'NO']
            elif LEVEL >= 30000:
                LUCK_LIST = ['PRO']
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
    """ # i will complete soon .
