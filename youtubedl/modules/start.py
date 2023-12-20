import pymongo
from hydrogram import Client, filters
from hydrogram.types import (
    InlineKeyboardButton as KeyboardButton,
    InlineKeyboardMarkup as KeyboardMarkup,
    Message as Msg,
    CallbackQuery as BackQuery
)
from youtubedl import ytdl
from youtubedl.database.mode_db import(
    get_normal_download_status,
    set_normal_download_status,
    get_playlist_download_status,
    set_playlist_download_status
)

start_keyboard = KeyboardMarkup([[
    KeyboardButton("📥 Normal Download", callback_data="nrml_dl"),
    KeyboardButton("Playlist Download 📂 ", callback_data="plylist_dl"),
    ],[
    KeyboardButton("❐ About", callback_data="about"),
    KeyboardButton("Help 📗 ", callback_data="help"),
    ],[
    KeyboardButton("⚙️ Settings", callback_data="settings")
    ]]
    )

help_keyboard = KeyboardMarkup([[
    KeyboardButton("Back ⏎", callback_data="back")
    ]]
    )

on_off_buttons = KeyboardMarkup([[
     KeyboardButton("✅ On", callback_data="on"), 
     KeyboardButton("Off ❌", callback_data="off"),
     ],[
     KeyboardButton("Back ⏎", callback_data="back")
     ]])

@ytdl.on_message(filters.command("start") & filters.private)
async def start(_, msg: Msg):
    user_id = msg.from_user.id
    normal_download_status = get_normal_download_status(user_id)
    playlist_download_status = get_playlist_download_status(user_id)
    status_text = f"Normal Download: {'✅ On' if normal_download_status else '❌ Off'}\nPlaylist Download: {'✅ On' if playlist_download_status else '❌ Off'}"
    start_text = f"**👋Hello {msg.from_user.mention()}**\n\nWelcome, I am a YouTube downloader bot. I can download YouTube videos or audios by searching and providing links and playlist links.👀\n\n**Developed By**: @TgBotsNetwork\n\n{status_text}"
    await msg.reply_text(
        text=start_text,
        reply_markup=start_keyboard
    )
    
@ytdl.on_callback_query(filters.regex("nrml_dl"))
async def nrml_dl_callback(client: Client, callback_query: BackQuery):
    await callback_query.edit_message_text(
        text="Choose an On/Off button to change mode:",
        reply_markup=on_off_buttons
    )

@ytdl.on_callback_query(filters.regex("plylist_dl"))
async def plylist_dl_callback(client: Client, callback_query: BackQuery):
    await callback_query.edit_message_text(
        text="Choose an On/Off button to change mode:",
        reply_markup=on_off_buttons
    )
    
@ytdl.on_callback_query(filters.regex(r"(?i)on|off"))
async def on_off_callback(client: Client, callback_query: BackQuery):
    user_id = callback_query.from_user.id
    command = callback_query.data  
    if "on" in command:
        status_text = "✅ On"
    elif "off" in command:
        status_text = "❌ Off"    
    if callback_query.data.endswith("nrml_dl"):
        set_normal_download_status(user_id, command)
    elif callback_query.data.endswith("plylist_dl"):
        set_playlist_download_status(user_id, command)  
    await callback_query.answer(f"Changed Current Settings: {status_text}", show_alert=True)

@ytdl.on_message(filters.command("help") & filters.private)
async def help(client: Client, msg: Msg):
    await msg.reply_text(
        text="<u><b>Help Section</b></u>\n\n- First, choose a mode in the start buttons: choose playlist mode or normal mode, and then send links from YouTube. Wait for a download, and the files will be saved.\n\n-<u><b>Available Commands</b></u>\n- /start: Start the bot and check if it's alive or not.\n- /help: Get information about the bot.",
        reply_markup=help_keyboard
    )

@ytdl.on_callback_query(filters.regex("back"))
async def back_callback(_, callback_query: BackQuery):
    user_id = callback_query.from_user.id
    normal_download_status = get_normal_download_status(user_id)
    playlist_download_status = get_playlist_download_status(user_id)
    status_text = f"Normal Download: {'✅ On' if normal_download_status else '❌ Off'}\nPlaylist Download: {'✅ On' if playlist_download_status else '❌ Off'}"
    start_text = f"**👋Hello {callback_query.message.from_user.mention()}**\n\nWelcome, I am a YouTube downloader bot. I can download YouTube videos or audios by searching and providing links and playlist links.👀\n\n**Developed By**: @TgBotsNetwork\n\n{status_text}"
    await callback_query.edit_message_text(
        text=start_text,
        reply_markup=start_keyboard
    )
    
@ytdl.on_callback_query(filters.regex("help"))
async def help(client: Client, callback_query: BackQuery):
    await callback_query.edit_message_text(
        text="<u><b>Help Section</b></u>\n\n- First, choose a mode in the start buttons: choose playlist mode or normal mode, and then send links from YouTube. Wait for a download, and the files will be saved.\n\n-<u><b>Available Commands</b></u>\n- /start: Start the bot and check if it's alive or not.\n- /help: Get information about the bot.",
        reply_markup=help_keyboard
    )

@ytdl.on_callback_query(filters.regex("about"))
async def help(client: Client, callback_query: BackQuery):
    await callback_query.edit_message_text(
        text="<u><b>About</b></u>\n\n**➫Language:** [Python](https://python.org)\n**➫Library:** [Hydrogram](https://hydrogram.amanoteam.com)\n**➫Developer:** @my_name_is_nobitha",
        disable_web_page_preview=True,
        reply_markup=help_keyboard
    )
