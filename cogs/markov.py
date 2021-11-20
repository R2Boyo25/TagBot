import discord
from discord.ext import commands
from utils.funcs import *
from database import Database as db
import subprocess, os

class MarkovCog(commands.Cog):
    '''Markov Commands'''
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command("markov")
    async def genMarkov(self, ctx, * , inputname):
        if not os.path.exists(f"./markov/cache/{inputname}"):
            await ctx.send("Cache file does not exist, generating....")
            os.system(f"./markov/mark ./markov/inputs/{inputname} to ./markov/cache/{inputname}")
        await ctx.send(subprocess.check_output(f"./markov/mark from ./markov/cache/{inputname} 200".split()).decode())
    
    @commands.command('inputs')
    async def markovInputs(self, ctx):
        await ctx.send(" ".join([i for i in os.listdir('./markov/inputs/')]))
    
    @commands.has_any_role(*Trusted)
    @commands.command('addinput')
    async def addMarkovInput(self, ctx, * , inputname):
        inputname = inputname.replace(" ", '-')
        if len(ctx.message.attachments) == 0:
            await ctx.send("Please attach a text file.")
        else:
            await ctx.message.attachments[0].save(f"./markov/inputs/{inputname}")

def setup(bot):
    bot.add_cog(MarkovCog(bot))
    