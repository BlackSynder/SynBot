from discord.ext import commands
import discord
import os
import asyncio


class Utilities:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, enabled=False)
    async def setavatar(self, ctx, picture):
        path = os.path.join("Bot Pics", picture)
        try:
            with open('%s' % path, 'rb') as f:
                await ctx.bot.user.edit(avatar=f.read())
            await ctx.send(":ok_hand: Avatar changed to %s" % picture.split(".")[0])
        except Exception:
            await ctx.send(":exclamation: File not found!")

    @commands.command()
    async def ping(self, ctx, message="Pong!"):
        await ctx.send(ctx.author.mention + " " + message)

def setup(bot):
    bot.add_cog(Utilities(bot))
