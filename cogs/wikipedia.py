import discord
from discord.ext import commands
from utils.funcs import *
from database import Database as db
import requests, urllib

class WikipediaCog(commands.Cog):
    '''Wikipedia Commands'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='wikipedia', aliases=['wiki'])
    async def Wikipedia(self, ctx, * , article):
        r = requests.get('https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles=' + urllib.parse.quote_plus(article).replace('+', '%20')).json()
        #await ctx.send(r)
        try:
            embed = discord.Embed(title=article.title(), description = r['query']['pages'][[i for i in r['query']['pages'].keys()][0]]['extract'].replace('\n', '\n\n').replace('.', '.\n'))
            await ctx.send(embed=embed)
        except:
            await ctx.send(f'Page {article.title()} not found')

def setup(bot):
    bot.add_cog(WikipediaCog(bot))
    
