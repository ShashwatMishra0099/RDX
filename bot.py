import os
from pyrogram import Client, filters
from youtube_dl import YoutubeDL
import ffmpeg
import asyncio
from pyrogram.types import Message

# Initialize the bot client with your API ID and API hash from Telegram
app = Client(
    "music_bot",
    api_id=os.environ["28165213"],
    api_hash=os.environ["74983137f88bb852802637dadf3d44a3"],
    bot_token=os.environ["7397084299:AAGzcPONLSvrdlHNYiQBsJXEV3TwGdPu_aY"]
)

# Function to download the audio from YouTube
def download_from_youtube(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'extractaudio': True,
        'audioformat': 'mp3',
    }
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(query, download=False)
        return info_dict['url'], info_dict['title']


# Command to play a song
@app.on_message(filters.command("play"))
async def play_song(client: Client, message: Message):
    query = message.text.split(" ", 1)[1]

    await message.reply("Searching for the song...")

    # Download or stream the song from YouTube
    url, title = download_from_youtube(f"ytsearch:{query}")

    await message.reply(f"Playing: {title}")

    # Join the voice chat (replace "your_chat_id" with the actual chat ID)
    chat_id = message.chat.id
    voice_chat = await client.get_chat(chat_id)
    await client.join_voice_chat(chat_id)

    # Stream the audio using FFmpeg
    process = (
        ffmpeg
        .input(url)
        .output("pipe:1", format="mp3")
        .run_async(pipe_stdout=True)
    )

    await asyncio.sleep(10)  # Simulate song playing for 10 seconds
    process.terminate()


# Command to pause the song
@app.on_message(filters.command("pause"))
async def pause_song(client: Client, message: Message):
    # In a real implementation, you'd control FFmpeg's process here
    await message.reply("Pausing the song...")


# Command to skip the song
@app.on_message(filters.command("skip"))
async def skip_song(client: Client, message: Message):
    # Terminate FFmpeg process here
    await message.reply("Skipping the song...")


# Command to stop the bot and leave the voice chat
@app.on_message(filters.command("stop"))
async def stop_song(client: Client, message: Message):
    chat_id = message.chat.id
    await client.leave_voice_chat(chat_id)
    await message.reply("Stopped the music and left the voice chat.")


# Start the bot
app.run()
