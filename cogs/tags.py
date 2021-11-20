import discord
from discord.ext import commands
from utils.funcs import *
from database import Database as db

class TagCog(commands.Cog):
    '''Tag Commands'''
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(name="tag", aliases=["t", "T", "ta", "TA", "TAG"])
    async def tag(self, ctx, tag):
        tag = tag.lower()

        if ctx.invoked_subcommand is None:

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

                await ctx.send(embed = embed)

            else:

                await ctx.send(f"Tag \"{tag}\" not found.")

    @commands.command(name="tagset", aliases=["ts", "TS" "TAGSET"])
    @commands.has_any_role(*Trusted)
    async def tagset(self, ctx, tagname, * , tagdesc:str):

        tagname = tagname.lower()

        database = db('tags.json')

        if len(ctx.message.attachments) > 0:

            database.set(tagname, {'text':tagdesc, 'image':ctx.message.attachments[0].url, 'author':ctx.author.id})
        
        else:

            database.set(tagname, {'text':tagdesc, 'author':ctx.author.id})

        await ctx.send(f"Tag \"{tagname}\" has been set.")

    @commands.command(name="taglist", aliases=["tl", "TL", "TAGLIST"])
    async def taglist(self, ctx):

        try:
            
            partfile = db('tags.json')

            with open(partfile.location) as json_file:

                keys = json.load(json_file)

            things=[]

            for thing in keys:

                things.append(f"**{thing}**")

            embeded = discord.Embed(title=f"Tags", description='\n'.join(things))

            await ctx.send(embed=embeded)

        except Exception as e:

            await ctx.send(f"Tags could not be retrieved.\nReason: {e}")
    
    @commands.command(name = 'deltag')
    @commands.has_any_role(*Trusted)
    async def deleteTag(self, ctx, tagname):
        tagname = tagname.lower()

        database = db('tags.json')

        database.delete(tagname)

        await ctx.send(f"Tag \"{tagname}\" has been deleted.")

def setup(bot):
    bot.add_cog(TagCog(bot))
    