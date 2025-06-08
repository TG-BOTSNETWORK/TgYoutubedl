import os
import re
import time
import asyncio
import requests
from PIL import Image
from hydrogram import Client, filters
from hydrogram.types import InlineKeyboardButton as Button, InlineKeyboardMarkup as Markup
from yt_dlp import YoutubeDL
from youtubedl import ytdl
from youtubedl.database.mode_db import get_is_on_off

# Regex for YouTube video and playlist
YOUTUBE_PLAYLIST_REGEX = re.compile(
    r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/(playlist\?list=|.*[?&]list=)([a-zA-Z0-9_-]+)"
)
YOUTUBE_VIDEO_REGEX = re.compile(
    r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/(watch\?v=|.*v=|.*be/)([a-zA-Z0-9_-]{11})"
)

def extract_video_id(url):
    match = re.search(r"(?:v=|youtu.be/|embed/|watch\?v=)([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else None

def get_video_info(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl = YoutubeDL({"quiet": True})
    return ydl.extract_info(url, download=False)

def download_video(video_id, quality="best[height<=1080]"):
    url = f"https://www.youtube.com/watch?v={video_id}"
    video_info = get_video_info(video_id)
    ydl_opts = {"format": quality, "outtmpl": f"{video_info['title']}.%(ext)s"}
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_audio(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    video_info = get_video_info(video_id)
    ydl_opts = {"format": "bestaudio", "outtmpl": f"{video_info['title']}.mp3"}
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@ytdl.on_message(filters.regex(r"(https?://(?:www\.)?(youtube\.com|youtu\.be)[^\s]+)"))
async def handle_youtube_links(client, message):
    url = message.matches[0].group(0)
    user_id = message.from_user.id

    is_nrml_enabled = get_is_on_off(user_id, mode="nrml")
    is_playlist_enabled = get_is_on_off(user_id, mode="playlist")

    if YOUTUBE_PLAYLIST_REGEX.match(url):
        if not is_playlist_enabled:
            return await message.reply_text("📛 Playlist download mode is off. Please enable it to proceed.")
        await process_playlist(client, message, url)

    elif YOUTUBE_VIDEO_REGEX.match(url):
        if not is_nrml_enabled:
            return await message.reply_text("📛 Normal video mode is off. Please enable it to proceed.")
        await process_single_video(client, message, url)

    else:
        await message.reply_text("⚠️ Unrecognized YouTube URL.")

async def process_single_video(client, message, url):
    video_id = extract_video_id(url)
    if not video_id:
        return await message.reply_text("Invalid video URL.")
    hmm = await message.reply_text("Processing your query...")
    await hmm.edit_text("Sending Audio/Video Options...")
    video_info = get_video_info(video_id)
    thumbnail_url = video_info["thumbnails"][-1]["url"]

    buttons = [[
        Button("🎥 Video", callback_data=f"download_video:{video_id}:video"),
        Button("🎶 Audio", callback_data=f"download_audio:{video_id}:audio")
    ]]
    await ytdl.send_photo(
        chat_id=message.chat.id,
        photo=thumbnail_url,
        caption=f"{video_info['title']}\n\nChoose download type:",
        reply_markup=Markup(buttons)
    )

async def process_playlist(client, message, url):
    hmm = await message.reply_text("📋 Getting playlist info...")
    try:
        ydl_opts = {"extract_flat": "in_playlist", "quiet": True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        playlist_title = info.get("title", "Playlist")
        entries = info.get("entries", [])

        await hmm.edit_text(f"🎶 Playlist: **{playlist_title}**\nTotal Videos: {len(entries)}")

        for entry in entries[:5]:  # Limit to 5 for demo
            video_url = f"https://www.youtube.com/watch?v={entry['id']}"
            await process_single_video(client, message, video_url)
            await asyncio.sleep(1)
    except Exception as e:
        await hmm.edit_text(f"❌ Error processing playlist: {str(e)}")

@ytdl.on_callback_query(filters.regex(r"download_video:(\S+):(\S+)"))
async def download_video_callback(client, callback_query):
    _, video_id, download_type = callback_query.data.split(":")
    chat_id = callback_query.message.chat.id
    msg = await callback_query.message.edit_text("Wait! Your Video is being found...")
    time.sleep(0.1)
    video_info = get_video_info(video_id)
    download_video(video_id, "best")
    share_keyboard = Markup([[Button("▶️ Youtube", url=f"https://www.youtube.com/watch?v={video_id}")]])
    file_path = f"{video_info['title']}.mp4"
    thumbnail_url = video_info["thumbnails"][-1]["url"]
    thumb_path = f"{video_info['title']}.jpg"
    thumbnail = Image.open(requests.get(thumbnail_url, stream=True).raw)
    thumbnail.save(thumb_path, format="JPEG")
    await msg.edit_text("Uploading your video...")
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
    video_info = get_video_info(video_id)
    download_audio(video_id)
    file_path = f"{video_info['title']}.mp3"
    thumbnail_url = video_info["thumbnails"][-1]["url"]
    thumb_path = f"{video_info['title']}.jpg"
    thumbnail = Image.open(requests.get(thumbnail_url, stream=True).raw)
    thumbnail.save(thumb_path, format="JPEG")
    if os.path.exists(file_path):
        with open(file_path, "rb") as audio_file:
            share_keyboard = Markup([[Button("▶️Youtube", url=f"https://www.youtube.com/watch?v={video_id}")]])
            await msg.edit_text("Uploading Your Audio....")
            await ytdl.send_audio(
                chat_id,
                audio=audio_file,
                caption=f"**Here is your audio:** {video_info['title']}\n\n**Developed By:** @my_name_is_nobitha",
                duration=int(video_info.get('duration', 0)),
                thumb=thumb_path,
                performer=video_info.get('channel_name', 'Unknown'),
                reply_markup=share_keyboard
            )
        os.remove(file_path)
        os.remove(thumb_path)
    else:
        await msg.edit_text("Error: Audio file not found.")
