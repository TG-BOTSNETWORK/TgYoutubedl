import asyncio
from hydrogram import Client, idle
from youtubedl import ytdl

async def main():
    try:
        chat_id = "5857041668"
        await ytdl.start()
        print("[Bot] - Ytdl Bot Started")
        await ytdl.send_message(chat_id, "Bot Started my dear owner bhai!")
        print("[Owner] - Started message sented to owner.")
    except Exception as e:
        print(f"{e}")
    await idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
