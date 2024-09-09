from telethon import TelegramClient, events
from pytgcalls import PyTgCalls, idle
from pytgcalls.types import Update
from pytgcalls.types.input_stream import InputAudioStream
import youtube_dl
import ffmpeg
import os

# Bot credentials
api_id = os.getenv("28165213")  # Replace with your API ID or set it in Heroku Config Vars
api_hash = os.getenv("74983137f88bb852802637dadf3d44a3")  # Replace with your API Hash or set it in Heroku Config Vars
bot_token = os.getenv("7397084299:AAGzcPONLSvrdlHNYiQBsJXEV3TwGdPu_aY")  # Replace with your Bot Token or set it in Heroku Config Vars

# Initialize Telegram bot client
bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Initialize PyTgCalls for voice chat
pytgcalls = PyTgCalls(bot)

# Join voice chat and stream music via FFmpeg
@bot.on(events.NewMessage(pattern='/play'))
async def play_music(event):
    chat_id = event.chat_id

    # Get the song name or URL
    song_name = event.text.split(" ", 1)[1]

    # Use youtube_dl to download the audio stream
    ydl_opts = {'format': 'bestaudio', 'noplaylist': True}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{song_name}", download=False)
        url = info['entries'][0]['url']

    # Join the voice chat
    await pytgcalls.join_group_call(
        chat_id,
        InputAudioStream(
            ffmpeg.input(url).output('-', format='s16le', acodec='pcm_s16le', ac=2, ar='48k').run_async(pipe_stdout=True)
        )
    )

    await event.respond(f"Playing: {info['entries'][0]['title']}")

# Start the PyTgCalls client
pytgcalls.start()

# Idle to keep the bot running
idle()
