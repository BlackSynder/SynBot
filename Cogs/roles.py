from discord.ext import commands
import discord
import os


class EmojiRoles:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def getroles(self, ctx):
        """Gets a list of all roles in the server"""
        response = "`Roles ID:`"
        for role in ctx.message.server.roles:
            if not role.is_everyone:
                if len(ctx.message.server.roles) > 15:
                    await ctx.bot.say(response)
                    response = "\n" + "Role name: %s ID: %s" % (role.name, role.id)
                else:
                    response += "\n" + "Role name: %s ID: %s" % (role.name, role.id)
        await ctx.bot.say(response)

def setup(bot):
    bot.add_cog(EmojiRoles(bot))
