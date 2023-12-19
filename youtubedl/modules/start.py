from hydrogram import Client, filters
from hydrogram.types import (
    InlineKeyboardButton as KeyboardButton,
    InlineKeyboardMarkup as KeyboardMarkup,
    Message as Msg,
    CallbackQuery as BackQuery
)
from youtubedl import ytdl

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
    KeyboardButton("Back⏎", callback_data="back")
    ]]
    )

@ytdl.on_message(filters.command("start") & filters.private)
async def start(client: Client, msg: Msg):
    await msg.reply_text(
        text=f"**👋Hello {msg.from_user.mention()}**\n\nWelcome, I am a YouTube downloader bot. I can download YouTube videos or audios by searching and providing links and playlist links.👀\n\n**Developed By**: @TgBotsNetwork",
        reply_markup=start_keyboard
    )

@ytdl.on_message(filters.command("help") & filters.private)
async def help(client: Client, msg: Msg):
    await msg.reply_text(
        text="<u><b>Help Section</b></u>\n\n- First you choose mode in start buttons choose a playlist mode or normal mode and then send links of youtube and wait fora downlaod and save that in files.\n\n-<u><b>Available Commands</b></u>\n- /start Start the bot check alive or not.\n- /help To know about bot deeply.",
        reply_markup=help_keyboard
    )

@ytdl.on_callback_query(filters.regex("back"))
async def back_callback(client: Client, callback_query: BackQuery):
    await callback_query.edit_message_text(
        text=f"**👋Hello {callback_query.msg.from_user.mention()}**\n\nWelcome, I am a YouTube downloader bot. I can download YouTube videos or audios by searching and providing links and playlist links.👀\n\n**Developed By**: @TgBotsNetwork",
        reply_markup=start_keyboard
    )

@ytdl.on_callback_query(filters.regex("help"))
async def help(client: Client, callback_query: BackQuery):
    await callback_query.edit_message_text(
        text="<u><b>Help Section</b></u>\n\n- First you choose mode in start buttons choose a playlist mode or normal mode and then send links of youtube and wait fora downlaod and save that in files.\n\n-<u><b>Available Commands</b></u>\n- /start Start the bot check alive or not.\n- /help To know about bot deeply.",
        reply_markup=help_keyboard
    )

@ytdl.on_callback_query(filters.regex("about"))
async def help(client: Client, callback_query: BackQuery):
    await callback_query.edit_message_text(
        text="<u><b>About</b></u>\n\n➫Language: [Python](https://python.org)\n➫Library: [Hydrogram](https://hydrogram.amanoteam.com)\n➫Developer: @my_name_is_nobitha",
        reply_markup=help_keyboard
    )
