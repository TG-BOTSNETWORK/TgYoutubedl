import os
import re
import asyncio
import time
import requests
from PIL import Image
from hydrogram import Client, filters
from hydrogram.types import InlineKeyboardButton as Button, InlineKeyboardMarkup as Markup
from youtubedl.database.mode_db import save_on_off, get_is_on_off
import yt_dlp

def extract_video_id(url):
    match = re.search(r"(?:v=|\/videos\/|embed\/|youtu.be\/|\/v\/|\/e\/|watch\?v=|&v=|%2Fvideos%2F|%2Fwatch%3Fv%3D|%2F|\?v=)([^#\\&\?]*)(?:[\w-]+)?", url)
    return match.group(1) if match else None

async def get_video_info(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "format": "best",
    }
    loop = asyncio.get_event_loop()
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=False))
    return info

async def download_file(video_id, download_type, chat_id, msg, quality="best[height<=1080]"):
    url = f"https://www.youtube.com/watch?v={video_id}"
    video_info = await get_video_info(video_id)
    file_ext = "mp3" if download_type == "audio" else "mp4"
    file_path = f"{video_info['title']}.{file_ext}"
    
    # Progress tracking
    progress_msg = await msg.edit_text("Starting download... [0%]")
    last_update = time.time()
    progress_data = {"percent": 0, "speed": 0, "eta": "N/A"}

    def progress_hook(d):
        nonlocal progress_data, last_update
        if d["status"] == "downloading":
            percent = d.get("downloaded_bytes", 0) / d.get("total_bytes", 1) * 100
            speed = d.get("speed", 0) / 1024 / 1024  # MB/s
            eta = d.get("eta", "N/A")
            progress_data = {"percent": percent, "speed": speed, "eta": eta}
            if time.time() - last_update >= 1:  # Update every second
                asyncio.create_task(update_progress(progress_msg, progress_data))
                last_update = time.time()

    async def update_progress(msg, data):
        bar = "█" * int(data["percent"] // 10) + "░" * (10 - int(data["percent"] // 10))
        text = f"Downloading... [{bar}] {data['percent']:.1f}%\nSpeed: {data['speed']:.2f} MB/s | ETA: {data['eta']}s"
        await msg.edit_text(text)

    ydl_opts = {
        "format": "bestaudio" if download_type == "audio" else quality,
        "outtmpl": file_path,
        "quiet": True,
        "noprogress": False,
        "progress_hooks": [progress_hook],
        "http_headers": {"User-Agent": "Mozilla/5.0"},
    }

    try:
        loop = asyncio.get_event_loop()
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            await loop.run_in_executor(None, lambda: ydl.download([url]))
        await progress_msg.edit_text("Download complete! Preparing upload...")
        return file_path, video_info
    except Exception as e:
        await progress_msg.edit_text(f"Error during download: {str(e)}")
        raise

async def save_thumbnail(video_info):
    thumbnail_url = video_info["thumbnails"][-1]["url"]
    thumb_path = f"{video_info['title']}.jpg"
    try:
        thumbnail = Image.open(requests.get(thumbnail_url, stream=True, timeout=5).raw)
        thumbnail.save(thumb_path, format="JPEG", quality=85)
        return thumb_path
    except Exception as e:
        print(f"Thumbnail error: {e}")
        return None

@ytdl.on_message(filters.regex(r"(https?://(?:www\.)?youtu\.be\S+|https?://(?:www\.)?youtube\.com\S+)"))
async def video_url(client, message):
    user_id = message.from_user.id
    is_nrml_enabled = get_is_on_off(user_id, mode="nrml")

    if not is_nrml_enabled:
        await message.reply_text("Normal download mode is currently off. Please go back and turn it on.")
        return

    url = message.matches[0].group(0)
    video_id = extract_video_id(url)
    if not video_id:
        await message.reply_text("Invalid YouTube URL.")
        return

    hmm = await message.reply_text("Processing your query...")
    await hmm.edit_text("Sending Audio/Video Options...")
    
    video_info = await get_video_info(video_id)
    thumbnail_url = video_info["thumbnails"][-1]["url"]

    reply_markup = Markup([
        [Button("🎥 Video", callback_data=f"download_video:{video_id}:video"),
         Button("Audio 🎶", callback_data=f"download_audio:{video_id}:audio")]
    ])

    await ytdl.send_photo(
        chat_id=message.chat.id,
        photo=thumbnail_url,
        caption=f"{video_info['title']}\n\nChoose download type:",
        reply_markup=reply_markup
    )
    await hmm.delete()

@ytdl.on_callback_query(filters.regex(r"download_(video|audio):(\S+):(\S+)"))
async def download_callback(client, callback_query):
    download_type, video_id, _ = callback_query.data.split(":")
    chat_id = callback_query.message.chat.id
    msg = await callback_query.message.edit_text("Wait! Processing your request...")

    try:
        file_path, video_info = await download_file(video_id, download_type, chat_id, msg)
        share_keyboard = Markup([[Button("▶️ Youtube", url=f"https://www.youtube.com/watch?v={video_id}")]])
        
        if download_type == "video":
            thumb_path = await save_thumbnail(video_info)
            await msg.edit_text("Uploading your video...")
            await ytdl.send_video(
                chat_id,
                video=file_path,
                caption=f"**Here is your video:** {video_info['title']}\n\n**Developed By:** @my_name_is_nobitha",
                reply_markup=share_keyboard,
                thumb=thumb_path,
                width=video_info.get('width', 1280),
                height=video_info.get('height', 720),
                duration=int(video_info.get('duration', 0)),
                supports_streaming=True
            )
            if thumb_path:
                os.remove(thumb_path)
        else:
            await msg.edit_text("Uploading your audio...")
            with open(file_path, "rb") as audio_file:
                await ytdl.send_audio(
                    chat_id,
                    audio=audio_file,
                    caption=f"**Here is your audio:** {video_info['title']}\n\n**Developed By:** @my_name_is_nobitha",
                    reply_markup=share_keyboard,
                    duration=int(video_info.get('duration', 0)),
                    title=video_info.get('title', 'Audio'),
                    performer=video_info.get('uploader', 'Unknown')
                )

        os.remove(file_path)
    except Exception as e:
        await msg.edit_text(f"Error: {str(e)}")
        if os.path.exists(file_path):
            os.remove(file_path)
        raise
