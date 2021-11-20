import discord
from discord.ext import commands
from utils.funcs import *
from database import Database as db
import json
import embedmenu

class AutorespondCog(commands.Cog):
    '''Autorespond Commands'''
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(name="ar")
    @commands.has_any_role(*Trusted)
    async def tag(self, ctx, *, tag):

        if ctx.invoked_subcommand is None:

            data = db("auto.json")

            if tag in data.keys():

                embed = discord.Embed(title = tag.title(), description = '```json\n' + json.dumps(data.get(tag), indent=4) + '\n```')

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

                await ctx.send(f"AutoResponse \"{tag}\" not found.")
    
    @commands.command(name="arset")
    @commands.has_any_role(*Trusted)
    async def tagset(self, ctx, arname, keyword, *, autoresponse):

        database = db("auto.json")

        database.set(arname, {'triggers':[arname], 'keyword':keyword, 'response':autoresponse, "author":ctx.author.id, 'exclusions':[]})

        await ctx.send(f"AR \"{arname}\" has been set.")

    @commands.command(name='arexclude')
    @commands.has_any_role(*Trusted)
    async def excludeChannelFromAutoResponse(self, ctx, arname, *channels):
        excludedchannels = [int(channel.strip("<#").strip(">")) for channel in channels]

        database = db('auto.json')
        try:
            a = database[arname]
        except:
            await ctx.send(f'Autoresponse \"{arname}\" does not exist.')
            return
        a['exclusions'] = excludedchannels
        database.set(arname, a)
        await ctx.send(f"Excluded channels for \"{arname}\" set to {excludedchannels}")

    @commands.command(name="arlist")
    @commands.has_any_role(*Trusted)
    async def taglist(self, ctx):

        try:
            
            partfile = db("auto.json")

            with open(partfile.location) as json_file:

                keys = json.load(json_file)

            things = [discord.Embed(title = "Autoresponses", description = "\n".join([str(thing) for thing in keys]))]

            for thing in keys:

                #things.append(f"**{thing}**")

                things.append(discord.Embed(title = thing, description = f"```json\n{json.dumps(partfile[thing], indent = 4)}\n```"))
            
            try:
                await embedmenu.embedMenu(self.bot, ctx, things)
            except:
                pass

            #embeded = discord.Embed(title=f"Setup Autoresponses", description='\n'.join(things))

            #await ctx.send(embed=embeded)

        except Exception as e:

            await ctx.send(f"Autoresponses could not be retrieved.\nReason: {e}")
    
    @commands.command(name = 'artag')
    @commands.has_any_role(*Trusted)
    async def addArTag(self, ctx, arname, tagname):
        database  = db('auto.json')

        try:
            a = database[arname]
        except:
            await ctx.send(f'Autoresponse \"{arname}\" does not exist.')
            return
        a['tag'] = tagname
        database.set(arname, a)
        await ctx.send(f"Tag for \"{arname}\" set to {tagname}")

        

    @commands.command(name = 'delar')
    @commands.has_any_role(*Trusted)
    async def deleteTag(self, ctx, tagname):

        database = db('tags.json')

        database.delete(tagname)

        await ctx.send(f"Autoresponse \"{tagname}\" has been deleted.")

def setup(bot):
    bot.add_cog(AutorespondCog(bot))
    