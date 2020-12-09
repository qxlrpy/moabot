# bot.py
import os
import discord
from discord import Embed
from discord import client
from discord.ext import commands
import datetime
import asyncio
import youtube_dl
from async_timeout import timeout
import discord.utils
from urllib import parse, request
import re
import random
from discord import Message
from discord.ext.commands import Context
import cogs
import functools
import itertools
import math
import random
import json
TOKEN = 'Nzc5MjQ4MjkxMjcwNzU0MzI0.X7dxhg.31W9p-N1lhNv45gW-fIogo34N5w'
bot = commands.Bot(command_prefix='m>', description="Moa Bot")

async def status_task():
    while True:
        await bot.change_presence(activity=discord.Streaming(name="m>help", url="http://www.twitch.tv/accountname"))
        await asyncio.sleep(15)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="MOA<3"))
        await asyncio.sleep(15)

@bot.command(brief="Shows bot latency.")
async def ping(ctx):
    await ctx.send('Pong!{0}'.format(round(bot.latency,1)))



@bot.command(brief="AFK command.")
async def afk(ctx, mins,reason):
    current_nick = ctx.author.nick
    await ctx.send(f"{ctx.author.mention} has gone afk for {mins} minutes.Reason: {reason}")

    counter = 0
    while counter <= int(mins):
        counter += 1
        await asyncio.sleep(60)

        if counter == int(mins):
            await ctx.author.edit(nick=current_nick)
            await ctx.send(f"{ctx.author.mention} is no longer AFK")
            break

@bot.command(brief="Clear command",description="Clear messages in specified amount.")
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)



@bot.command(brief="Announcement command.",ignore_extra=False)
async def announce(ctx, channel, *message):
    color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    channel = channel.replace('<#', '')
    channel = int(channel.replace('>', ''))
    channe = bot.get_channel(channel)
    message = (" ".join(message[0:]))
    embed = discord.Embed(title="Announcement", description=f"{message}", color=color)
    await channe.send(embed=embed)
    

@bot.command(brief="Shows server info.")
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="MOA CLAN DISCORD SERVER", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Owner", value=f"#arda'#6969")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    # embed.set_thumbnail(url=f"{ctx.guild.icon}")
    embed.set_thumbnail(url="https://pluralsight.imgix.net/paths/python-7be70baaac.png")

    await ctx.send(embed=embed)

@bot.command(brief="Bot joins voice channel.")
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


# Events
@bot.event
async def on_ready():
    print('-------------------------')     
    print('Giriş Yaptım!')                  
    print('Botun İsmi : ' + bot.user.name)  
    print('ID   : ' + str(bot.user.id))
    print(f"discord.py versiyon: {discord.__version__}")
    print("Bot Komut Bilgileri\nKomut Sayısı {0}.Komutlarda aktif {1} \n".format(
        str(len(bot.cogs)), str(len(bot.commands))))     
    print('Made by qxlrpy')           
    print('-------------------------')    
    bot.loop.create_task(status_task())
    
async def on_member_join(member):
    for channel in member.guild.channels:
        if str(channel) == "general": # We check to make sure we are sending the message in the general channel
            await channel.send_message(f"""Welcome to the server {member.mention}""")

@bot.listen('on_message')
async def napim(message):
    if message.content.lower().startswith("napim"):
        await message.add_reaction("😎")

async def onmessage(message):
    with open("users.json", "r") as f:
        users = json.load(f)

        if message.author.bot:
            return
        if message.channel.is_private:
            return
        else:
            await update_data(users, message.author, message.server)
            number = random.randint(5,10)
            await add_experience(users, message.author, number, message.server)
            await level_up(users, message.author, message.channel, message.server)

        with open("users.json", "w") as f:
            json.dump(users, f)
    await bot.process_commands(message)

async def update_data(users, user, server):
    if not user.id + "-" + server.id in users:
        users[user.id + "-" + server.id] = {}
        users[user.id + "-" + server.id]["experience"] = 0
        users[user.id + "-" + server.id]["level"] = 1
        users[user.id + "-" + server.id]["last_message"] = 0

async def add_experience(users, user, exp, server):
    if time.time() - users[user.id + "-" + server.id]["last_message"] > 30: 
        users[user.id + "-" + server.id]["experience"] += exp
        users[user.id + "-" + server.id]["last_message"] = time.time()
    else:
        return

async def level_up(users, user, channel, server):
    experience = users[user.id + "-" + server.id]["experience"]
    lvl_start = users[user.id + "-" + server.id]["level"]
    lvl_end = int(experience ** (1/4))

    if lvl_start < lvl_end:
        await bot.send_message(channel, f":tada: Congrats {user.mention}, you levelled up to level {lvl_end}!")
        users[user.id + "-" + server.id]["level"] = lvl_end




bot.run('Nzc5MjQ4MjkxMjcwNzU0MzI0.X7dxhg.31W9p-N1lhNv45gW-fIogo34N5w')


