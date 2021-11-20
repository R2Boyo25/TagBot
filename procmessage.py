import discord
from utils.funcs import *
from database import Database as db
from difflib import get_close_matches as cMatches

def isTrusted(roles):
    troles = []
    for role in roles:
        if role.id in Trusted:
            troles.append(role.id)
    return len(troles)>0

async def processMessage(message, bot):
    autoresponses = db('auto.json')
    tags = db('tags.json')
    
    if (len(message.content) > 0) and (not isTrusted(message.author.roles)):
        if message.content.lower()[0] in 'abcdefghijklmnopqrstuvwxyz1234567890':
            for i in autoresponses.keys():
                if (
                    len(
                        cMatches(
                            message.content.lower().strip(), 
                            [*autoresponses[i]['triggers']]
                        )
                    ) > 0 
                    and autoresponses[i]['keyword'].lower() 
                    in message.content.lower().strip() 
                    and 
                    (message.channel.id not in autoresponses[i]['exclusions'])
                    ):
                    if 'tag' in autoresponses[i]:
                        if autoresponses[i]['tag'] in tags.keys():
                            
                            tag = autoresponses[i]['tag']
                            if tags[tag]['text'].count("\n") < 1 and 'image' not in tags[tag]:
                            
                                await message.channel.send(tags[tag]['text'])

                            else:

                                embed = discord.Embed(title = tag, description = tags[tag]['text'])

                                try:
                                    embed.set_image(url = tags[tag]['image'])
                                except KeyError:
                                    pass
                                
                                try:
                                    author = message.guild.get_member(int(tags[tag]['author']))
                                    try:
                                        if author.nick == None:
                                            raise Exception('e')
                                        embed.set_author(name = author.nick, icon_url = author.avatar_url)
                                    except:
                                        embed.set_author(name = author.name, icon_url = author.avatar_url)
                                except:
                                    pass

                                await message.channel.send(embed = embed)
                    else:
                        await message.channel.send(autoresponses[i]['response'])
                    break
    #if len(cMatches(message.content.lower().strip(), ["where can i find help"])) > 0 and "help" in message.content.lower().strip():
    #    await message.channel.send("<#871031669866500096> , <#204648659248218113>, or <#394965670523043840> for help.")
    #if message.content.startswith(";") and not message.content.startswith(";take") and message.channel != bot.get_channel(323186380379389952):
    #    await message.channel.send("Commands go in <#323186380379389952>")
