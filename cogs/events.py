import discord, traceback, os
from utils.funcs import *
from database import Database as db
import procmessage

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
            await message.channel.send("You poinged? do .help (or [yourserverseprefix]help)")


        await bot.process_commands(message)
    