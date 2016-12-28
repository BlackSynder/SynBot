from discord.ext import commands
import discord
import asyncio
import os


class Administration:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def wl(self, ctx):
        """
        Manages the whitelist.\nIn order to use this command you need to be an admin.
        """
        if ctx.invoked_subcommand is None:
            await ctx.bot.say("Invalid Command. Use ``syn help`` for more info")

    @wl.command(pass_context=True)
    async def add(self, ctx, member: discord.Member):
        """
        Adds a user to the whitelist.\nUsers in the whitelist can use advanced commands.\n\nCommands:\n~delete\n~role\n~assign
        """
        if not self.bot.is_admin(ctx.message.author.id):
            response = "You're not allowed to use this command! :angry:"
            await ctx.bot.say(response)
            async for log in ctx.bot.logs_from(ctx.message.channel, limit=5):  # deletes the response
                if log.content == response:
                    asyncio.sleep(5)
                    await ctx.bot.delete_message(log)
        else:
            if self.bot.is_whitelisted(ctx.message.server.id, member.id):
                await ctx.bot.say("%s is already in the whitelist!" % member.name)
            else:
                string = '%s\n' % member.id
                filename = "whitelist-%s.txt" % ctx.message.server.id
                path = os.path.join("Server Configs", filename)
                with open(path, "a") as f:
                    f.write(string)
                await ctx.bot.say("Successfully added %s to the whitelist! :ok_hand:" % member.name)

    @wl.command(pass_context=True)
    async def remove(self, ctx, member: discord.Member):
        """
        Removes a user from the whitelist.\nOnce this is issued, the user will forever be removed. Use the add command to readd to the whitelist.
        """
        if not self.bot.is_admin(ctx.message.author.id):
            response = "You're not allowed to use this command! :angry:"
            await ctx.bot.say(response)
            async for log in ctx.bot.logs_from(ctx.message.channel, limit=5):  # deletes the response
                if log.content == response:
                    asyncio.sleep(5)
                    await ctx.bot.delete_message(log)
                    await ctx.bot.delete_message(ctx.message)
        else:
            if self.bot.is_whitelisted(ctx.message.server.id, member.id):
                filename = "whitelist-%s.txt" % ctx.message.server.id
                path = os.path.join("Server Configs", filename)
                with open(path, "r+") as f:
                    lines = f.readlines()
                    f.seek(0)
                    for line in lines:
                        if not line.startswith(member.id):
                            f.write(line)
                    f.truncate()
                response = "Removed %s from the whitelist successfully :ok_hand:" % member.name
                await ctx.bot.say(response)
                async for log in ctx.bot.logs_from(ctx.message.channel, limit=5):  # deletes the response
                    if log.content == response:
                        asyncio.sleep(5)
                        await ctx.bot.delete_message(log)
                        await ctx.bot.delete_message(ctx.message)
            else:
                response = "%s is not whitelisted!" % member.name
                await ctx.bot.say(response)
                async for log in ctx.bot.logs_from(ctx.message.channel, limit=5):  # deletes the response
                    if log.content == response:
                        asyncio.sleep(5)
                        await ctx.bot.delete_message(log)
                        await ctx.bot.delete_message(ctx.message)


def setup(bot):
    bot.add_cog(Administration(bot))
