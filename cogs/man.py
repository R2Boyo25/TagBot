import discord
from discord.ext import commands
from utils.funcs import *
from database import Database as db
import subprocess, textwrap, re, asyncio

async def sayLongLineEmbeded(text, ctx, title, wrap_at=1990):

    for number, line in enumerate(
                            textwrap.wrap(
                                re.sub(r'(?<=[.,])(?=[^\s])', r' ', str(text)).replace(
                                                "\n", "/n" 
                                            ), 
                                        wrap_at 
                                    ) 
                                ):

        l = line.replace("/n", "\n").replace('\\n', '\n')

        embed = discord.Embed(
            title = f"{title}", 
            description = f'```\n{l}\n```', 
            )

        await ctx.send(embed = embed)
        await asyncio.sleep(3)

class ManCog(commands.Cog):
    '''Man Commands'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command('man')
    async def getManual(self, ctx, *, man):
        #try:
        e = subprocess.check_output(f"man {man}".split())

        await sayLongLineEmbeded(e.decode(), ctx, man)
        #except:
        #    await ctx.send(f'No manual for {man} found')

def setup(bot):
    bot.add_cog(ManCog(bot))
    