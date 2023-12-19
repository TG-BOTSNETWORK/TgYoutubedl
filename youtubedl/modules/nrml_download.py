import os
from hydrogram import Client, filters
from hydrogram.types import (
    InlineKeyboardButton as Button,
    InlineKeyboardMarkup as Markup,
    Message as Msg,
    CallbackQuery
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

def get_video_info(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl = YoutubeDL()
    info = ydl.extract_info(url, download=False)
    return info


def download_video(video_id, quality="best"):
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        "format": quality,
        "outtmpl": f"{video_id}.%(ext)s",
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


@ytdl.on_message(filters.incoming & filters.text)
def handle_text_message(client, message):
    query = message.text.strip()
    results = YoutubeSearch(query, max_results=1).to_dict()

    if results:
        video_info = get_video_info(results[0]["id"])
        thumbnail_url = video_info["thumbnails"][-1]["url"]

        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Video", callback_data=f"download_video:{results[0]['id']}:video"),
             InlineKeyboardButton("Audio", callback_data=f"download_video:{results[0]['id']}:audio")]
        ])

        ytdl.send_photo(chat_id=message.chat.id, photo=thumbnail_url,
                          caption=f"{video_info['title']}\n\nChoose download type:", reply_markup=reply_markup)


@ytdl.on_callback_query(filters.regex(r"download_video:(\S+):(\S+)"))
def download_callback(client, callback_query):
    _, video_id, download_type = callback_query.data.split(":")
    download_video(video_id, "best" if download_type == "video" else "bestaudio")

    file_path = f"{video_id}.{'mp4' if download_type == 'video' else 'webm'}"
    ytdl.send_document(chat_id=callback_query.message.chat.id, document=file_path,
                         caption="Here is your video/audio.")
    os.remove(file_path)
