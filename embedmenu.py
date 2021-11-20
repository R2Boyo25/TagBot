import discord
from discord.ext import commands


async def embedMenu(bot, ctx, pages):
    message = await ctx.send(embed = pages[0])

    await message.add_reaction('⏮')
    await message.add_reaction('◀')
    await message.add_reaction('▶')
    await message.add_reaction('⏭')
    await message.add_reaction('🗑️')

    def check(reaction, user):
        return reaction.message.id == message.id and user.id == ctx.author.id

    i = 0
    emoji = ''

    while True:
        if emoji == '⏮':
            i = 0
            await message.edit(embed = pages[i])

        elif emoji == '◀':
            if i > 0:
                i -= 1
                await message.edit(embed = pages[i])

        elif emoji == '▶':
            if i < len(pages) - 1:
                i += 1
                await message.edit(embed = pages[i])

        elif emoji == '⏭':
            i = len(pages) - 1
            await message.edit(embed = pages[i])

        elif emoji == "🗑️":
            await message.delete()
            return
        
        try:
            es = await bot.wait_for('reaction_add', timeout = 30.0, check = check)
        except:
            await message.delete()
            break

        if res == None:
            break

        if res[1] != bot:
            emoji = str(res[0].emoji)
            try:
                await message.remove_reaction(res[0].emoji, res[1])
            except:
                pass