import os
from hydrogram import Client, filters
from hydrogram.types import (
    InlineKeyboardButton as Button,
    InlineKeyboardMarkup as Markup,
    Message as Msg
)
from youtubesearch import YoutubeSearch
from yt_dlp import YoutubeDL
from PIL import Image
from youtubedl import ytdl

DOWNLOAD_DIR = "downloads/"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

AUDIO_QUALITIES = ["low", "medium", "high"]
VIDEO_QUALITIES = ["144p", "240p", "360p", "480p", "720p", "1080p"]

def download_media(url, quality, is_audio=True):
    options = {
        "format": f"bestaudio[abr={quality}]" if is_audio else f"bestvideo[height={quality}]",
        "outtmpl": DOWNLOAD_DIR + "%(title)s.%(ext)s",
    }
    with YoutubeDL(options) as ydl:
        ydl.download([url])

def get_thumbnail(url):
    with YoutubeDL({"outtmpl": "%(title)s.%(ext)s"}) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        thumbnail_url = info_dict.get("thumbnail", "")
        return thumbnail_url

@ytdl.on_message(filters.incoming & filters.text)
async def handle_message(client: Client, msg: Msg):
    text = msg.text
    if "youtube.com" in text or "youtu.be" in text:
        video_id = text.split("v=")[1] if "youtube.com" in text else text.split("/")[-1]
        quality_buttons = [
            [
                Button(text=f"Download {quality.capitalize()} Quality",
                       callback_data=f"{quality}_{video_id}")
            ] for quality in VIDEO_QUALITIES
        ]
        keyboard = Markup(quality_buttons)
        await msg.reply_text(
            text="Choose video quality:",
            reply_markup=keyboard
        )
    else:
        videos = YoutubeSearch(text, max_results=1).to_dict()
        if videos:
            video_id = videos[0]["id"]
            thumbnail_url = get_thumbnail(f"https://www.youtube.com/watch?v={video_id}")
            quality_buttons = [
                [
                    Button(text=f"Download {quality.capitalize()} Quality",
                           callback_data=f"{quality}_{video_id}")
                ] for quality in AUDIO_QUALITIES
            ]

            keyboard = Markup(quality_buttons)
            await msg.reply_photo(
                photo=thumbnail_url,
                caption="Choose audio quality:",
                reply_markup=keyboard
            )
        else:
            await msg.reply_text("No results found.")

@ytdl.on_callback_query()
async def handle_callback_query(client: Client, query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id
    quality, video_id = data.split("_")
    download_media(f"https://www.youtube.com/watch?v={video_id}", quality, is_audio=("low" in quality or "medium" in quality or "high" in quality))
    await query.message.reply_video(
        video=DOWNLOAD_DIR + f"{video_id}.mp4",
        caption="This is your requested video."
    )
