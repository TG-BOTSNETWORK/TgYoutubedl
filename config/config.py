from os import getenv
from dotenv import load_dotenv

load_dotenv()
que = {}
admins = {}

API_ID = int(getenv("API_ID", "11163590"))
API_HASH = getenv("API_HASH", "fa76f31e5f7a64d906d4978dd0e5d3b3")
BOT_TOKEN = getenv("BOT_TOKEN","6932413042:AAF9ZtiWN82C764wQlmrhSFqlbjWoHfBtg0")
BOT_NAME = getenv("BOT_NAME","Tg Youtube Download")
DB_URI = getenv("DB_URI", "postgres://doqtmbqn:6vuttQBYuDdh-Gts7A8J21CEBh7lvByp@berry.db.elephantsql.com/doqtmbqn")
