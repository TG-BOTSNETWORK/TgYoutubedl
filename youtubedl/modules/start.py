from hydrogram import Client, filters
from hydrogram.types import (
    InlineKeyboardButton as KeyboardButton,
    InlineKeyboardMarkup as KeyboardMarkup,
    Message as Msg,
    CallbackQuery as BackQuery
)
from youtubedl import ytdl
from youtubedl.database.mode_db import (
    save_on_off,
    get_is_on_off
)
import capitalize

start_keyboard = KeyboardMarkup([[
    KeyboardButton("📥 Normal Download", callback_data="nrml_dl"),
    KeyboardButton("Playlist Download 📂 ", callback_data="plylist_dl"),
], [
    KeyboardButton("❐ About", callback_data="about"),
    KeyboardButton("Help 📗 ", callback_data="help"),
], [
    KeyboardButton("⚙️ Settings", callback_data="settings")
]])

help_keyboard = KeyboardMarkup([[
    KeyboardButton("Back ⏎", callback_data="back")
]])

on_off_buttons = KeyboardMarkup([[
    KeyboardButton("✅ On", callback_data="on"),
    KeyboardButton("Off ❌", callback_data="off"),
], [
    KeyboardButton("Back ⏎", callback_data="back")
]])

@ytdl.on_message(filters.command("start") & filters.private)
async def start(_, msg: Msg):
    user_id = msg.from_user.id
    status_nrml = get_is_on_off(user_id)
    status_playlist = get_is_on_off(user_id)
    status_text_nrml = f"Normal Download: {'✅ On' if status_nrml else '❌ Off'}"
    status_text_playlist = f"Playlist Download: {'✅ On' if status_playlist else '❌ Off'}"    
    start_text = f"**👋Hello {msg.from_user.mention()}**\n\nWelcome, I am a YouTube downloader bot. I can download YouTube videos or audios by searching and providing links and playlist links.👀\n\n**Developed By**: @TgBotsNetwork\n\n{status_text_nrml}\n{status_text_playlist}"  
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

ytdl.on_callback_query(filters.regex(r"(?i)on|off"))
async def on_off_callback(client: Client, callback_query: BackQuery):
    user_id = callback_query.from_user.id
    command = callback_query.data
    mode = "nrml" if callback_query.data.endswith("nrml_dl") else "playlist"
    status = True if "on" in command else False
    status_text = "✅ On" if status else "❌ Off"
    save_on_off(user_id, status)   
    await callback_query.answer(f"Changed {mode.capitalize()} Download Settings: {status_text}", show_alert=True)
 
@ytdl.on_message(filters.command("help") & filters.private)
async def help(client: Client, msg: Msg):
    await msg.reply_text(
        text="<u><b>Help Section</b></u>\n\n- First, choose a mode in the start buttons: choose playlist mode or normal mode, and then send links from YouTube. Wait for a download, and the files will be saved.\n\n-<u><b>Available Commands</b></u>\n- /start: Start the bot and check if it's alive or not.\n- /help: Get information about the bot.",
        reply_markup=help_keyboard
    )

@ytdl.on_callback_query(filters.regex("back"))
async def back_callback(_, callback_query: BackQuery):
    user_id = callback_query.from_user.id
    status_nrml = get_is_on_off(user_id, "normal")
    status_playlist = get_is_on_off(user_id, "playlist")
    status_text_nrml = f"Normal Download: {'✅ On' if status_nrml else '❌ Off'}"
    status_text_playlist = f"Playlist Download: {'✅ On' if status_playlist else '❌ Off'}"    
    start_text = f"**👋Hello {callback_query.message.from_user.mention()}**\n\nWelcome, I am a YouTube downloader bot. I can download YouTube videos or audios by searching and providing links and playlist links.👀\n\n**Developed By**: @TgBotsNetwork\n\n{status_text_nrml}\n{status_text_playlist}"
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
