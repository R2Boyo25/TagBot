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
        '''
        if (
            ' wor ' in message.content.lower() 
            or 
            message.content.lower().endswith(' wor') 
            or 
            message.content.lower().startswith('wor ')
            or 
            message.content.lower().strip() == 'wor'
            ):
            await message.add_reaction('🤮')

        if (
            ' twister ' in message.content.lower() 
            or 
            message.content.lower().endswith(' twister') 
            or 
            message.content.lower().startswith('twister ')
            or 
            message.content.lower().strip() == 'twister'
            ):
            await message.add_reaction('🤮')
        
        if (
            ' twisteros ' in message.content.lower() 
            or 
            message.content.lower().endswith(' twisteros') 
            or 
            message.content.lower().startswith('twisteros ')
            or 
            message.content.lower().strip() == 'twisteros'
            ):
            await message.add_reaction('🤮')
        
        if (
            ' biden ' in message.content.lower() 
            or 
            message.content.lower().endswith(' biden') 
            or 
            message.content.lower().startswith('biden ')
            or 
            message.content.lower().strip() == 'biden'
            ):
            await message.add_reaction('<:biden:897678984719003698>')

        if (
            ' router ' in message.content.lower() 
            or 
            message.content.lower().endswith(' router') 
            or 
            message.content.lower().startswith('router ')
            or 
            message.content.lower().strip() == 'router'
            ):
            await message.add_reaction('<:router_hands:840674797359726602>')

        if (
            ' cope ' in message.content.lower() 
            or 
            message.content.lower().endswith(' cope') 
            or 
            message.content.lower().startswith('cope ')
            or 
            message.content.lower().strip() == 'cope'
            ):
            await message.add_reaction('<:copium:872279045004492861>')
        
        if (
            ' copium ' in message.content.lower() 
            or 
            message.content.lower().endswith(' copium') 
            or 
            message.content.lower().startswith('copium ')
            or 
            message.content.lower().strip() == 'copium'
            ):
            await message.add_reaction('<:copium:872279045004492861>')

        if (
            ' debian ' in message.content.lower() 
            or 
            message.content.lower().endswith(' debian') 
            or 
            message.content.lower().startswith('debian ')
            or 
            message.content.lower().strip() == 'debian'
            ):
            await message.add_reaction('<:debian:891389275894083655>')
        
        if (
            ' pog ' in message.content.lower() 
            or 
            message.content.lower().endswith(' pog') 
            or 
            message.content.lower().startswith('pog ')
            or 
            message.content.lower().strip() == 'pog'
            ):
            await message.add_reaction('<:pogpaul:726625782780264489>')

        if (
            ' plorange ' in message.content.lower() 
            or 
            message.content.lower().endswith(' plorange') 
            or 
            message.content.lower().startswith('plorange ')
            or 
            message.content.lower().strip() == 'plorange'
            ):
            await message.add_reaction('<:plorange:711698778087751750>')
        '''
        if message.channel.id == 217477797319409676:
            await message.add_reaction("👋")
            return 

        await procmessage.processMessage(message, bot)

        if str(message.content).replace(' ', '') == bot.user.mention: 
            await message.channel.send("You poinged? do .help (or [yourserverseprefifix]help)")


        await bot.process_commands(message)
    