import discord
from discord.ext import commands
from utils.funcs import *
from database import Database as db
import traceback

class MathCog(commands.Cog):
    '''Math Commands'''
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='1var')
    @commands.has_any_role(*Trusted)
    async def var1(self, ctx, num:int, *, formula:str):
        count = 0
        a = []
        for x in range(int("-"+str(num)), int(num)):
            if eval(formula.lower().replace("a", str(x)).replace("x", str(x)).replace("=", "==").replace("====", "==").strip('`')):
                a.append(f'x = {x}')
                count = count + 1

        a.append(f"{count} solutions.")

        embed = discord.Embed(description = "\n".join(a))
        await ctx.send(embed=embed)
    
    @var1.error
    async def var1error(self, ctx, error):
        e = []
        for ii, i in enumerate(traceback.format_exception(type(error), error, error.__traceback__)[4:]):
            if i.strip().startswith('\n'):
                break
            else:
                e.append(i)
        await ctx.channel.send('```py\n' + ''.join(e) + '\n```')
        ctx.handled = True

def setup(bot):
    bot.add_cog(MathCog(bot))
    