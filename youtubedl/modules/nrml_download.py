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

DOWNLOAD_DIR = "downloads/"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

AUDIO_QUALITIES = ["low", "medium", "high"]
VIDEO_QUALITIES = ["144p", "240p", "360p", "480p", "720p", "1080p"]

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
        "outtmpl": f"{DOWNLOAD_DIR}/{video_id}.%(ext)s",  # Save in DOWNLOAD_DIR
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        
def download_audio(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": f"{DOWNLOAD_DIR}/{video_id}.mp3",
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@ytdl.on_message(filters.incoming & filters.text)
def handle_text_message(client, message):
    query = message.text.strip()
    video_id = extract_video_id(query)

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

    if download_type == "video":
        ytdl.send_message(chat_id, text="Wait! Your video is being found...")

        download_video(video_id, "best")

        file_path = f"{DOWNLOAD_DIR}/{video_id}.mp4"
        ytdl.send_message(chat_id, text="Uploading your video...")
        ytdl.send_video(chat_id, video=file_path, caption="Here is your video.")
        os.remove(file_path)

@ytdl.on_callback_query(filters.regex(r"download_audio:(\S+)"))
def download_audio_callback(client, callback_query):
    video_id = callback_query.matches[0].group(1)
    chat_id = callback_query.message.chat.id
    ytdl.send_message(chat_id, text="Wait! Your audio is being found...")

    download_audio(video_id)

    file_path = f"{DOWNLOAD_DIR}/{video_id}.mp3"
    if os.path.exists(file_path):
        with open(file_path, "rb") as audio_file:
            ytdl.send_audio(chat_id, audio=audio_file, caption="Here is your audio.")
        os.remove(file_path)
    else:
        ytdl.send_message(chat_id, text="Error: Audio file not found.")
