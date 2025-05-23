from hydrogram import Client, filters
from hydrogram.types import (
    InlineKeyboardButton as KeyboardButton,
    InlineKeyboardMarkup as KeyboardMarkup,
    Message as Msg,
    CallbackQuery as BackQuery
)
from youtubedl.database.mode_db import (
    save_on_off,
    get_is_on_off
)
from youtubedl import ytdl
import time
from datetime import datetime

start_keyboard = KeyboardMarkup([[
    KeyboardButton("📥 Normal Download", callback_data="nrml_dl"),
    KeyboardButton("Playlist Download 📂 ", callback_data="playlist_dl"),
], [
    KeyboardButton("❐ About", callback_data="about"),
    KeyboardButton("Help 📗 ", callback_data="help"),
    ]])

help_keyboard = KeyboardMarkup([[
    KeyboardButton("Back ⏎", callback_data="back")
]])

playlist_on_off_buttons = KeyboardMarkup([[
    KeyboardButton("✅ On", callback_data="playlist_dl_on"),
    KeyboardButton("Off ❌", callback_data="playlist_dl_off"),
], [
    KeyboardButton("Back ⏎", callback_data="back")
]])

nrml_on_off_buttons = KeyboardMarkup([[
    KeyboardButton("✅ On", callback_data="nrml_dl_on"),
    KeyboardButton("Off ❌", callback_data="nrml_dl_off"),
], [
    KeyboardButton("Back ⏎", callback_data="back")
]])

@ytdl.on_message(filters.command("start") & filters.private)
async def start(_, msg: Msg):
    user_id = msg.from_user.id
    status_nrml = get_is_on_off(user_id, mode="nrml")
    status_playlist = get_is_on_off(user_id, mode="playlist")
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
        reply_markup=nrml_on_off_buttons
    )

@ytdl.on_callback_query(filters.regex("playlist_dl"))
async def playlist_dl_callback(client: Client, callback_query: BackQuery):
    await callback_query.edit_message_text(
        text="Choose an On/Off button to change mode:",
        reply_markup=playlist_on_off_buttons
    )

@ytdl.on_callback_query(filters.regex(r"(?i)playlist_dl_(on|off)"))
async def playlist_dl_callback(client: Client, callback_query: BackQuery):
    user_id = callback_query.from_user.id
    command = callback_query.data
    status = True if "on" in command else False
    status_text = "✅ On" if status else "❌ Off"
    save_on_off(user_id, normal_status=False, playlist_status=status)  
    status_nrml, status_playlist = get_is_on_off(user_id, mode="both")
    status_text_nrml = f"Normal Download: {'❌ Off'}"  # Set normal status explicitly to '❌ Off'
    status_text_playlist = f"Playlist Download: {'✅ On' if status_playlist else '❌ Off'}"
    start_text = f"**👋Hello {callback_query.message.from_user.mention()}**\n\nWelcome, I am a YouTube downloader bot. I can download YouTube videos or audios by searching and providing links and playlist links.👀\n\n**Developed By**: @TgBotsNetwork\n\n{status_text_nrml}\n{status_text_playlist}"  
    start_text += f"\nLast edited: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    await callback_query.answer(f"Changed Playlist Download Settings: {status_text}", show_alert=True)
    await callback_query.edit_message_text(
        text=start_text,
        reply_markup=start_keyboard
    )

@ytdl.on_callback_query(filters.regex(r"(?i)nrml_dl_(on|off)"))
async def nrml_dl_callback(client: Client, callback_query: BackQuery):
    user_id = callback_query.from_user.id
    command = callback_query.data
    status = True if "on" in command else False
    status_text = "✅ On" if status else "❌ Off"    
    save_on_off(user_id, playlist_status=False, normal_status=status) 
    status_nrml, _ = get_is_on_off(user_id, mode="both")
    status_text_nrml = f"Normal Download: {'✅ On' if status_nrml else '❌ Off'}"
    status_text_playlist = f"Playlist Download: {'❌ Off'}"  # Set playlist status explicitly to '❌ Off'
    new_start_text = f"**👋Hello {callback_query.message.from_user.mention()}**\n\nWelcome, I am a YouTube downloader bot. I can download YouTube videos or audios by searching and providing links and playlist links.👀\n\n**Developed By**: @TgBotsNetwork\n\n{status_text_nrml}\n{status_text_playlist}"
    new_start_text += f"\nLast edited: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    await callback_query.answer(f"Changed Normal Download Settings: {status_text}", show_alert=True)
    await callback_query.edit_message_text(
        text=new_start_text,
        reply_markup=start_keyboard
    )

@ytdl.on_message(filters.command("help") & filters.private)
async def help(client: Client, msg: Msg):
    await msg.reply_text(
        text="<u><b>Help Section</b></u>\n\n- First, choose a mode in the start buttons: choose playlist mode or normal mode, and then send links from YouTube. Wait for a download, and the files will be saved.\n\n-<u><b>Available Commands</b></u>\n- /start: Start the bot and check if it's alive or not.\n- /help: Get information about the bot.",
        reply_markup=help_keyboard
    )

@ytdl.on_callback_query(filters.regex("back"))
async def back_callback(_, callback_query: BackQuery):
    user_id = callback_query.from_user.id
    status_nrml, status_playlist = get_is_on_off(user_id, mode="both")
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
