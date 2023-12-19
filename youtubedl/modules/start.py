from hydrogram import Client, filters
from hydrogram.types import (
    InlineKeyboardButton as KeyboardButton,
    InlineKeyboardMarkup as KeyboardMarkup,
    Message as Msg
)
from youtubedl import ytdl

start_keyboard = KeyboardMarkup([
    KeyboardButton("📥 Normal Download", callback_data="nrml_dl"),
    KeyboardButton("📂 Playlist Download", callback_data="plylist_dl"),
    ],[
    KeyboardButton("⚙️ Settings", callback_data="settings")
    ])


@ytdl.on_message(filters.command("start"))
async def start_handler(client: Client, msg: Msg):
    await msg.reply_text(
        text=f"**👋Hello {msg.from_user.mention()}**\nWelcome, I am a YouTube downloader bot. I can download YouTube videos or audios by searching and providing links and playlist links.👀\n\n**Developed By**: @TgBotsNetwork",
        reply_markup=start_keyboard
    )
else:
     await msg.reply_text("Start me in Dm")
