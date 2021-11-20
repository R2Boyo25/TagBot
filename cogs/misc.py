import discord
from discord.ext import commands
from utils.funcs import *
from database import Database as db

class MiscCog(commands.Cog):
    '''Misc Commands'''
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(name='delmsg', hidden=True)
    @commands.has_any_role(*Trusted)
    async def delBotMsg(self, ctx, message:discord.Message):
        #await ctx.message.delete()
        if message.author == self.bot.user:
            await message.delete()
    

    @commands.command(name='math', hidden=True)
    @commands.has_any_role(*Trusted)
    async def mathCom(self, ctx, *, com):
        await ctx.send(str(eval(com)))

def setup(bot):
    bot.add_cog(MiscCog(bot))
    