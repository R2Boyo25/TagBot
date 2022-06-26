import discord, traceback, os
from utils.funcs import *
from database import Database as db
import procmessage

async def tag(ctx, message):
    tag = message.lstrip("??").lower()

    data = db("tags.json")

    if tag in data.keys():

        embed = discord.Embed(title = tag, description = data[tag]['text'])

        try:
            embed.set_image(url = data[tag]['image'])
        except KeyError:
            pass
        try:
            author = ctx.guild.get_member(int(data[tag]['author']))
            try:
                embed.set_author(name = author.nick, icon_url = author.avatar_url)
            except:
                embed.set_author(name = author.name, icon_url = author.avatar_url)
        except:
            pass

        await ctx.channel.send(embed = embed)

    else:
        if tag.strip() != "":
            await ctx.channel.send(f"Tag \"{tag}\" not found.")

def setup(bot):
    @bot.event
    async def on_ready():

        channel = bot.get_channel(logChannel)
        msg = await channel.send('Bot Has Rebooted')

        sum = len(set(bot.get_all_members()))

        print('logged in as {}'.format(bot.user))

        status = f"over {len(bot.guilds)} servers, {sum} users | .help"
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))

    @bot.event
    async def on_message(message):

        if message.author == bot.user:
            return
        
        if message.content.startswith("??"):
            await tag(message, message.content)
            return
        
        for word in config('reactions').keys():
            ml = message.content.lower()
            word = word.lower()
            if (f' {word} ' in ml or ml.endswith(f' {word}') or ml.startswith(f'{word} ') or ml.strip() == word):
                await message.add_reaction(config('reactions')[word])

        if message.channel.id == 217477797319409676:
            await message.add_reaction("👋")
            return 

        await procmessage.processMessage(message, bot)

        if str(message.content).replace(' ', '') == bot.user.mention: 
            await message.channel.send("You pinged? do .help (or [yourserverseprefix]help)")

        await bot.process_commands(message)
