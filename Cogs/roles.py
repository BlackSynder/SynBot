from discord.ext import commands
import discord
import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from paginator import Pages

class Roles:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roles(self, ctx):
        """Gets a list of all roles in the server"""
        try:
            p = Pages(self.bot, message=ctx.message, entries=[r.mention for r in ctx.guild.roles if not r.is_default])
            p.embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon)
            await p.paginate()
        except Exception as e:
            await ctx.send(e)

def setup(bot):
    bot.add_cog(Roles(bot))
