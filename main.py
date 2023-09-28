import os
import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio
from fastapi import FastAPI
import uvicorn

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

music_queue = []


@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))


@bot.command()
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()


@bot.command()
async def play(ctx, *, song_name_or_url):
    voice_client = ctx.voice_client
    if voice_client and voice_client.is_playing():
        music_queue.append(song_name_or_url)
        await ctx.send("Added to queue!")
    else:
        if not voice_client:
            channel = ctx.message.author.voice.channel
            await channel.connect()
        await play_music(ctx, song_name_or_url)


@bot.command()
async def stop(ctx):
    await stop_music(ctx)


@bot.command()
async def skip(ctx):
    try:
        voice_client = ctx.voice_client
        if voice_client.is_playing():
            os.remove('song.mp3')
            voice_client.stop()
            await ctx.send("Music skipped!")
    except AttributeError:
        await ctx.send("Not currently playing any music.")


async def play_music(ctx, song_name_or_url):
    # Configurar as opções do youtube-dl
    ytdl_options = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': 'song.mp3',
        'nocheckcertificate': True,
        'noplaylist': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

    search_keyword = song_name_or_url

    if "http" not in song_name_or_url:
        search_keyword = f"ytsearch:{song_name_or_url}"

    # Fazer o download da música
    with youtube_dl.YoutubeDL(ytdl_options) as ytdl:
        info = ytdl.extract_info(search_keyword, download=True)
        yt_file = ytdl.prepare_filename(info)

    # Conectar ao canal de voz do usuário
    voice_client = ctx.voice_client
    if not voice_client:
        channel = ctx.author.voice.channel
        voice_client = await channel.connect()

    # Tocar a música
    source = discord.FFmpegPCMAudio(yt_file)
    voice_client.play(source)

    # Esperar até a música terminar de tocar
    while voice_client.is_playing():
        await asyncio.sleep(1)

    if len(music_queue) > 0:
        os.remove(yt_file)
        await play_music(ctx, music_queue.pop(0))
    else:
        # Desconectar do canal de voz
        await voice_client.disconnect()
        os.remove(yt_file)


async def stop_music(ctx):
    music_queue.clear()
    voice_client = ctx.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        await voice_client.disconnect()
        await ctx.send(f"{ctx.author.name} stopped the player!")

app = FastAPI()


@app.get("/health")
async def health_check():
    return {"status": "OK"}


async def run_bot():
    await bot.start(os.environ["DISCORD_TOKEN"])

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    bot_task = loop.create_task(run_bot())

    async def run_web_server():
        config = uvicorn.Config(app, host="0.0.0.0", port=8080)
        server = uvicorn.Server(config)
        await server.serve()

    web_server_task = loop.create_task(run_web_server())

    try:
        loop.run_until_complete(asyncio.gather(bot_task, web_server_task))
    except KeyboardInterrupt:
        loop.run_until_complete(bot.close())
