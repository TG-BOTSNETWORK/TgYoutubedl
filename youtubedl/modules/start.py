from hydrogram import Client, filters
from hydrogram.types import(
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
async def(client, msg: Msg):
    await msg.reply_text( 
        text=f"**👋Hello {}**\nWelcome iam an Youtube downloader bot i can download a youtube videos or audios with searching and providing links and playlist links.👀\n\n**Developed By**: @TgBotsNetwork".format(msg.from_user.mention()),
        reply_markup=start_keyboard
    )
else:
    await msg.reply_text("Start me in Dm")
