import discord
from discord.ext import commands
from utils.funcs import *
from database import Database as db

class LogCog(commands.Cog):
    '''Log Commands'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command('getmsgs', hidden = True)
    async def getmsgs(self, ctx, author:discord.Member, channel:discord.TextChannel, amount:int):
        def check(message):
            return message.author.id == author.id

        msgs = []

        try:
            async for message in channel.history(limit=amount):
                if message.author.id == author.id:
                    msgs.append(message.content)
        except discord.errors.Forbidden:
            pass
        except AttributeError:
            pass
        
        with open(f'{author.id}.txt', 'w') as f:
            f.write('\n'.join(msgs))
        
        await ctx.send(ctx.author.mention, file=discord.File(f'{author.id}.txt'))

def setup(bot):
    bot.add_cog(LogCog(bot))
    