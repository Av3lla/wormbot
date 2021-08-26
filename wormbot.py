import os
import discord
from discord.ext import commands, tasks
import asyncio
import hcskr
import youtube_dl


bot = commands.Bot(command_prefix='/')


@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'commands.{extension}')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'commands.{extension}')

@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f'commands.{extension}')
    bot.load_extension(f'commands.{extension}')

for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        bot.load_extension(f"commands.{filename[:-3]}")


@bot.event
async def on_ready():
    print("---연결 성공 ---")
    print(f"봇 이름: {bot.user.name}")
    print(f"ID: {bot.user.id}")
    await bot.change_presence(activity=discord.Game("/도움말"))


@bot.command()
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("""지금 듣고있는 음악이 끝날 때 까지 기다리거나 "/stop" 커맨드를 사용해서 중지하세요""")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name="그냥음성대화")
    await voiceChannel.connect()
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    

@bot.command()
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    elif not voice.is_connected():
        await ctx.send("아직 벌레봇이 통화방에 없습니다.")


@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    elif not voice.is_playing():
        await ctx.send("아직 벌레봇이 노래를 듣고 있지 않습니다.")


@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_pause():
        voice.resume()
    elif not voice.is_pause():
        await ctx.send("아직 벌레봇이 노래를 일시정지 하지 않았습니다.")


@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()


TOKEN = "NzQ4MTE1MDAzMTM1MDk4OTEw.X0YuZA.uWI8RYzNcNdkc-UEOCblv_N-9sk"
bot.run(TOKEN)