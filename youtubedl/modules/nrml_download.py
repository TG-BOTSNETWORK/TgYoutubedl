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

DOWNLOAD_DIR = "downloads/"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


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

def download_video(video_id, quality="best"):
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        "format": quality,
        "outtmpl": f"{DOWNLOAD_DIR}/{video_id}.%(ext)s",
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_audio(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": f"{DOWNLOAD_DIR}/{video_id}.mp3",
        "postprocessors": [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@ytdl.on_message(filters.text & ~filters.command(["start", "help", "stats", "broadcast", "settings"]))
def handle_text_message(client, message):
    query = message.text.strip()
    video_id = extract_video_id(query)
    hmm = message.reply_text("Processing your query")
    hmm.edit_text("Sending Audio Video Modes....")
    if video_id:
        video_info = get_video_info(video_id)
        thumbnail_url = video_info["thumbnails"][-1]["url"]

        reply_markup = Markup([
            [Button("Video", callback_data=f"download_video:{video_id}:video"),
             Button("Audio", callback_data=f"download_audio:{video_id}:audio")]
        ])

        ytdl.send_photo(chat_id=message.chat.id, photo=thumbnail_url,
                          caption=f"{video_info['title']}\n\nChoose download type:", reply_markup=reply_markup)

@ytdl.on_callback_query(filters.regex(r"download_video:(\S+):(\S+)"))
def download_video_callback(client, callback_query):
    _, video_id, download_type = callback_query.data.split(":")
    chat_id = callback_query.message.chat.id
    msg = callback_query.message.edit_text("Wait! Your Video is being found...")
    asyncio.sleep(0.1)
    msg.edit_text("Found your Video....")
    asyncio.sleep(0.1)
    msg.edit_text("URL checking....")
    if download_type == "video":
        download_video(video_id, "best")
        share_keyboard = Markup([[
                Button("Youtube", url=f"https://www.youtube.com/watch?v={video_id}")
                ]]
                )
        file_path = f"{DOWNLOAD_DIR}/{video_info['title']}.mp4"
        asyncio.sleep(0.1)
        msg.edit_text(chat_id, text="Uploading your video...")
        asyncio.sleep(2)
        ytdl.send_video(chat_id, video=file_path, caption=f"Here is your video: {video_info['title']}\n\nDeveloped By: @my_name_is_nobitha", reply_markup=share_keyboard)
        os.remove(file_path)

@ytdl.on_callback_query(filters.regex(r"download_audio:(\S+)"))
def download_audio_callback(client, callback_query):
    video_id = callback_query.matches[0].group(1)
    chat_id = callback_query.message.chat.id
    msg = callback_query.message.edit_text("Wait! Your audio is being found...")
    asyncio.sleep(0.1)
    msg.edit_text("Found your audio....")
    asyncio.sleep(0.1)
    msg.edit_text("URL checking....")
    download_audio(video_id)
    share_keyboard = Markup([[
        Button("Youtube", url=f"https://www.youtube.com/watch?v={video_id}")
    ]])
    file_path = f"{DOWNLOAD_DIR}/{video_info['title']}.mp3"
    asyncio.sleep(0.1)
    msg.edit_text("Uploading Your Audio....")
    asyncio.sleep(2)
    if os.path.exists(file_path):
        with open(file_path, "rb") as audio_file:
            ytdl.send_audio(chat_id, audio=audio_file, caption=f"Here is your audio: {video_info['title']}\n\nDeveloped By: @my_name_is_nobitha", reply_markup=share_keyboard)
        os.remove(file_path)
    else:
        ytdl.send_message(chat_id, text="Error: Audio file not found.")        
