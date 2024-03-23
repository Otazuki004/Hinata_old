from pyrogram import *
from pyrogram.types import *

from Hinata import *
from Hinata.Database.main import *

async def add_item(user_id: int, item_id: int):
    doc = {'player': user_id, 'item_id': item_id, 'quantity': 1}
    result = await db.inventory.find_one(doc)
    if not result:
        result = await db.inventory.insert_one(doc)
    else:
        return None

async def increase_item(user_id: int, item_id: int):
    filter = {'player': user_id, 'item_id': item_id}
    update = {'$inc': {'quantity': 1}}
    result = await db.inventory.update_one(filter, update)
    return None

async def get_item(user_id: int, item_id: int):
    filter = {'player': user_id, 'item_id': item_id}
    item = await db.inventory.find_one(filter)
    if item:
        return item
    else:
        return False


items = {
1 : {"name" : "Regular Sword", "cost" : 10, "sell_cost" : 8, "item_type" : "weapon", "item_symbol" : "🗡️", "hp" : 0, "mana" : 0, "attack" : 2,
                             "magic_attack" : 0, "armour" : 0, "magic_armour" : 0, "req_level" : 1, "availability" : 1},
2 : {"name" : "Dual Edge Sword", "cost" : 25, "sell_cost" : 15, "item_type" : "weapon", "item_symbol" : "🗡️", "hp" : 0, "mana" : 0, "attack" : 4,
                            "magic_attack" : 0, "armour" : 0, "magic_armour" : 0, "req_level" : 2, "availability" : 2},
3 : {"name" : "Holy Sword", "cost" : 70, "sell_cost" : 55, "item_type" : "weapon", "item_symbol" : "🗡️", "hp" : 0, "mana" : 0, "attack" : 7,
                            "magic_attack" : 0, "armour" : 0, "magic_armour" : 0, "req_level" : 3, "availability" : 3},
4 : {"name" : "Common Staff", "cost" : 10, "sell_cost" : 8, "item_type" : "weapon", "item_symbol" : "🗡️", "hp" : 0, "mana" : 0, "attack" : 0,
                            "magic_attack" : 2, "armour" : 0, "magic_armour" : 0, "req_level" : 1, "availability" : 1},
5 : {"name" : "Rare Staff", "cost" : 25, "sell_cost" : 15, "item_type" : "weapon", "item_symbol" : "🗡️", "hp" : 0, "mana" : 0, "attack" : 0,
                              "magic_attack" : 4, "armour" : 0, "magic_armour" : 0, "req_level" : 2, "availability" : 2},
6 : {"name" : "Old Jacket", "cost" : 10, "sell_cost" : 8, "item_type" : "armour", "item_symbol" : "🛡️", "hp" : 5, "mana" : 0, "attack" : 0,
                           "magic_attack" : 0, "armour" : 2, "magic_armour" : 0, "req_level" : 1, "availability" : 1},
7 : {"name" : "Strong Jacket", "cost" : 20, "sell_cost" : 18, "item_type" : "armour", "item_symbol" : "🛡️", "hp" : 10, "mana" : 0, "attack" : 0,
                              "magic_attack" : 0, "armour" : 4, "magic_armour" : 0, "req_level" : 2, "availability" : 2},
8 : {"name" : "Regular Helmet", "cost" : 5, "sell_cost" : 3, "item_type" : "helmet", "item_symbol" : "⛑️", "hp" : 2, "mana" : 0, "attack" : 0,
                              "magic_attack" : 0, "armour" : 1, "magic_armour" : 0, "req_level" : 1, "availability" : 1},
9 : {"name" : "Regular Boots", "cost" : 4, "sell_cost" : 2, "item_type" : "boots", "item_symbol" : "👢", "hp" : 2, "mana" : 0, "attack" : 0,
                             "magic_attack" : 0, "armour" : 1, "magic_armour" : 0, "req_level" : 1, "availability" : 1},
10 : {"name" : "Health Potion", "cost" : 5, "sell_cost" : 3, "item_type" : "potion", "item_symbol" : "🔮", "hp" : 5, "mana" : 0, "attack" : 0,
                          "magic_attack" : 0, "armour" : 0, "magic_armour" : 0, "req_level" : 1, "availability" : 1}
}

@app.on_message(filters.command("shop"))
async def shop(client: Client, message: Message):
    close_shop = InlineKeyboardButton("Close 🚫", callback_data=f"close_{message.from_user.id}")
    y = {}
    for x in items.values():
        if not x.get("item_type") in y:
            y[x.get("item_type")] = x.get("item_symbol")
        else:
            pass

    type_buttons = [
        InlineKeyboardButton(
            f"Buy {item_type[0].capitalize()}{ 's' if item_type[0][-1]!='s' else ''} {item_type[1]}",
            callback_data=f"show_{message.from_user.id}_{item_type[0]}"
        ) for item_type in y.items()
    ]

    buttons = [type_buttons[i:i+2] for i in range(0, len(type_buttons), 2)]
    markup = InlineKeyboardMarkup([[button for button in row] for row in buttons])
    markup.inline_keyboard.append([close_shop])
    await message.reply_text(
        "🛒 **Welcome To Shop!**", 
        reply_markup=markup, 
        parse_mode=enums.ParseMode.MARKDOWN
  )

@app.on_callback_query(filters.regex("close"))
async def close_cq(_, cq):
    user_id = int(cq.data.split("_")[1])
    if cq.from_user.id == user_id:
        await cq.message.delete()
    else:
        await cq.answer("This Wasn't Requested By You")

@app.on_callback_query(filters.regex("buy"))
async def buy_cq(_, cq):
    user_id = int(cq.data.split("_")[1])
    item_id = int(cq.data.split("_")[2])
    back_reply = InlineKeyboardButton("Back 🔙", callback_data=f"backshop_{user_id}")
    back_shop = InlineKeyboardMarkup([[back_reply]])
    if cq.from_user.id == user_id:
        money = await GET_COINS_FROM_USER(user_id)
        item = await items.get(item_id)
        if money < item['cost']:
            await cq.message.edit_text("`Not Enough Coins.`", reply_markup=back_shop, parse_mode=enums.ParseMode.MARKDOWN)
        else:
            money -= item['cost']
            await ADD_COINS(cq.from_user.id, -money)
            is_already = await get_item(cq.from_user.id, item_id)
            if not is_already:
                await add_item(cq.from_user.id, item_id)
            else:
                await increase_item(cq.from_user.id, item_id)
            await cq.message.edit_text(f"**You Bought An Item** `{item['name']}`. **You Now Have Them In Your Inventory** .", reply_markup=back_shop, parse_mode=enums.ParseMode.MARKDOWN)

@app.on_callback_query(filters.regex("show"))
async def show_items_by_type_cq(client: Client, cq: CallbackQuery):
    user_id = int(cq.data.split("_")[1])
    item_type = cq.data.split("_")[2]
    back_shop = InlineKeyboardButton("Back 🔙", callback_data=f"backshop_{cq.from_user.id}")
    if cq.from_user.id == user_id:
        items_list = [item for item in items.values() if item.get("item_type") == str(item_type)]
        if not items_list:
            await cq.message.edit_text("`No items to show.`", reply_markup=InlineKeyboardMarkup([[back_shop]]))
        else:
            buttons = []
            for item in items_list:
                buttons.append([
                    InlineKeyboardButton(f"{item['name']} - {item['cost']} coins", callback_data=f"buy_{user_id}_{item['id']}")
                ])
            buttons.append([back_shop])
            await cq.message.edit_text(f"**Items of type {item_type}:**", reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await cq.answer("This Wasn't Requested By You")

@app.on_callback_query(filters.regex("backshop"))
async def back_shop_cq(client: Client, cq: CallbackQuery):
    user_id = int(cq.data.split("_")[1])
    if not cq.from_user.id == user_id:
        return await cq.answer("This Wasn't Requested By You")
    else:
        close_shop = InlineKeyboardButton("Close 🚫", callback_data=f"close_{user_id}")
        y = {}
        for x in items.values():
            if not x.get("item_type") in y:
                y[x.get("item_type")] = x.get("item_symbol")
            else:
                pass

        type_buttons = [
            InlineKeyboardButton(
                f"Buy {item_type[0].capitalize()}{ 's' if item_type[0][-1]!='s' else ''} {item_type[1]}",
                callback_data=f"show_{user_id}_{item_type[0]}"
            ) for item_type in y.items()
        ]

        buttons = [type_buttons[i:i+2] for i in range(0, len(type_buttons), 2)]
        markup = InlineKeyboardMarkup([[button for button in row] for row in buttons])
        markup.inline_keyboard.append([close_shop])
        await cq.edit_message_text(
            "🛒 **Welcome To Shop!**", 
            reply_markup=markup, 
            parse_mode=enums.ParseMode.MARKDOWN
  )
      
  
