from Cogs.paginator import Pages

from discord.ext import commands


class Roles:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roles(self, ctx):
        """Gets a list of all roles in the server"""
        try:
            roles = [r.mention for r in ctx.guild.roles if not r.is_default()]
            p = Pages(self.bot, message=ctx.message, entries=roles)
            p.embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
            await p.paginate()
        except Exception as e:
            await ctx.send(e)


def setup(bot):
    bot.add_cog(Roles(bot))
