from os import getenv
from dotenv import load_dotenv

load_dotenv()
que = {}
admins = {}

API_ID = int(getenv("API_ID", "11163590"))
API_HASH = getenv("API_HASH", "fa76f31e5f7a64d906d4978dd0e5d3b3")
BOT_TOKEN = getenv("BOT_TOKEN","7785265477:AAHj4DLXsbAnRwQ2UzKaTkXq7mcn5GkbTKA")
BOT_NAME = getenv("BOT_NAME","Tg Youtube Download")
