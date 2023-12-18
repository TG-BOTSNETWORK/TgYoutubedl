import asyncio
from hydrogram import Client, idle
from youtubedl import ytdl

async def main():
    try:
        await ytdl.start()
        print("[Bot] - Ytdl Bot Started")
        await ytdl.join_chat("https://t.me/TgBotsNetwork")
        print("[Join chat] - Successfully joined in chat")
    except Exception as e:
        print(f"{e}")
    await idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
