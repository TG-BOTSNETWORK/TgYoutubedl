import os
from hydrogram import Client, filters
from hydrogram.types import (
    InlineKeyboardButton as Button,
    InlineKeyboardMarkup as Markup,
)
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL
from youtubedl import ytdl
import yt_dlp
import re
import asyncio
import time
import requests
from PIL import Image

def extract_video_id(url):
    match = re.search(r"(?:v=|\/videos\/|embed\/|youtu.be\/|\/v\/|\/e\/|watch\?v=|&v=|%2Fvideos%2F|%2Fwatch%3Fv%3D|%2F|\?v=)([^#\\&\?]*)(?:[\w-]+)?", url)
    if match:
        return match.group(1)
    else:
        return None

def get_video_info(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl = YoutubeDL()
    info = ydl.extract_info(url, download=False)
    return info

def download_video(video_id, quality="best[height<=1080]"):
    url = f"https://www.youtube.com/watch?v={video_id}"
    video_info = get_video_info(video_id)
    ydl_opts = {
        "format": quality,
        "outtmpl": f"{video_info['title']}.%(ext)s",
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_audio(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    video_info = get_video_info(video_id)
    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": f"{video_info['title']}.mp3",
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@ytdl.on_message(filters.regex(r"(https?://(?:www\.)?youtu\.be\S+|https?://(?:www\.)?youtube\.com\S+)"))
async def video_url(client, message):
    url = message.matches[0].group(0)
    video_id = extract_video_id(url)
    hmm = await message.reply_text("Processing your query")
    await hmm.edit_text("Sending Audio Video Modes....")
    if video_id:
        video_info = get_video_info(video_id)
        thumbnail_url = video_info["thumbnails"][-1]["url"]

        reply_markup = Markup([
            [Button("🎥 Video", callback_data=f"download_video:{video_id}:video"),
             Button("Audio 🎶", callback_data=f"download_audio:{video_id}:audio")]
        ])

        await ytdl.send_photo(chat_id=message.chat.id, photo=thumbnail_url,
                          caption=f"{video_info['title']}\n\nChoose download type:", reply_markup=reply_markup)

@ytdl.on_callback_query(filters.regex(r"download_video:(\S+):(\S+)"))
async def download_video_callback(client, callback_query):
    _, video_id, download_type = callback_query.data.split(":")
    chat_id = callback_query.message.chat.id
    msg = await callback_query.message.edit_text("Wait! Your Video is being found...")
    await time.sleep(0.1)
    await msg.edit_text("Found your Video....")
    await time.sleep(0.1)
    await msg.edit_text("URL checking....")
    video_info = get_video_info(video_id)
    if download_type == "video":
        download_video(video_id, "best")
        share_keyboard = Markup([[
            Button("▶️ Youtube", url=f"https://www.youtube.com/watch?v={video_id}")
        ]])
        file_path = f"{video_info['title']}.mp4"
        thumbnail_url = video_info["thumbnails"][-1]["url"]
        thumb_path = f"{video_info['title']}.jpg"
        thumbnail = Image.open(requests.get(thumbnail_url, stream=True).raw)
        thumbnail.save(thumb_path, format="JPEG")
        await time.sleep(0.1)
        await msg.edit_text("Uploading your video...")
        await time.sleep(2)
        await ytdl.send_video(
            chat_id,
            video=file_path,
            caption=f"**Here is your video:** {video_info['title']}\n\n**Developed By:** @my_name_is_nobitha",
            reply_markup=share_keyboard,
            thumb=thumb_path,
            width=video_info.get('width', 1280),
            height=video_info.get('height', 720),
            duration=video_info.get('duration', 0),
        )
        os.remove(file_path)
        os.remove(thumb_path)
        
@ytdl.on_callback_query(filters.regex(r"download_audio:(\S+)"))
async def download_audio_callback(client, callback_query):
    video_id = callback_query.matches[0].group(1)
    chat_id = callback_query.message.chat.id
    msg = await callback_query.message.edit_text("Wait! Searching for a Audio...")
    await time.sleep(0.1)
    await msg.edit_text("Founded your Audio....")
    try:
        video_info = get_video_info(video_id)
        download_audio(video_id)
        await time.sleep(2)
        file_path = f"{video_info['title']}.mp3"
        if os.path.exists(file_path):
            with open(file_path, "rb") as audio_file:
                share_keyboard = Markup([[
                    Button("▶️Youtube", url=f"https://www.youtube.com/watch?v={video_id}")
                ]])
                await msg.edit_text("Uploading Your Audio....")
                await ytdl.send_audio(
                    chat_id,
                    audio=audio_file,
                    caption=f"**Here is your audio:** {video_info['title']}\n\n**Developed By:** @my_name_is_nobitha",
                    reply_markup=share_keyboard
                )
                os.remove(file_path)
        else:
            await msg.edit_text("Error: Audio file not found.")
    except Exception as e:
        await msg.edit_text(f"Error: {str(e)}")
