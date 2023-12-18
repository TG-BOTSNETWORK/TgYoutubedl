from hydrogram import Client
from config.config import API_ID, API_HASH, BOT_TOKEN

ytdl = Client(
     "ytdlbot",
     api_id=API_ID,
     api_hash=API_HASH,
     bot_token=BOT_TOKEN,
     plugins=dict(root="youtubedl.modules")
)
