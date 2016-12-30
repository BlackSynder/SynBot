from discord.ext import commands
import discord
import os
import asyncio


class Utilities:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, hidden=True)
    async def setavatar(self, ctx, picture):
        path = os.path.join("Bot Pics", picture)
        try:
            with open('%s' % path, 'rb') as f:
                await ctx.bot.edit_profile(avatar=f.read())
            await ctx.bot.say(":ok_hand: Avatar changed to %s" % picture.split(".")[0])
        except Exception:
            await ctx.bot.say(":exclamation: File not found!")

    @commands.command(pass_context=True)
    async def ping(self, ctx, message="Pong!"):
        await ctx.bot.say(ctx.message.author.mention + " " + message)

    @commands.group(pass_context=True)
    async def delete(self, ctx):
        """
        A command used to mass delete messages.\nThis command deletes the last messages in the channel its invoked in. Use either from or amount.
        """
        if ctx.invoked_subcommand is None:
            await ctx.bot.say("Invalid Command. Use ``syn help`` for more info")

    @delete.command(pass_context=True)
    async def upto(self, ctx, date):
        """
        This sets a date for the command to delete up to.\nFor example, if I wanted to delete all messages sent in the last week, I'd use !delete upto <date seven days ago>\nThe limit for this command is 500 messages
        """

        if self.bot.is_whitelisted(ctx.message.server.id, ctx.message.author.id):  # checks if allowed to delete
            count = 0
            async for log in ctx.bot.logs_from(ctx.message.channel, limit=500):  # loop for deletion
                msg_date = "".join(str(log.timestamp).split(" ")[0].split("-"))
                deadline = "".join(str(date).split("-"))
                if msg_date > deadline:
                    await ctx.bot.delete_message(log)
                    count += 1
            response = "Successfully deleted %s messages" % count
            await ctx.bot.say(response)
            async for log in ctx.bot.logs_from(ctx.message.channel, limit=5):  # deletes the response
                if log.content == response:
                    asyncio.sleep(5)
                    await ctx.bot.delete_message(log)
                    print("%s has deleted %s messages in %s(%s)" % (ctx.message.author.name, count, ctx.message.channel, ctx.message.server))
        else:
            response = "You're not allowed to use this command!"
            await ctx.bot.say(response)
            async for log in ctx.bot.logs_from(ctx.message.channel, limit=5):  # deletes the response
                if log.content == response:
                    asyncio.sleep(5)
                    await ctx.bot.delete_message(log)
                    await ctx.bot.delete_message(ctx.message)
            print("%s tried to delete messages but isn't allowed." % ctx.message.author.name)

    @delete.command(pass_context=True)
    async def amount(self, ctx, msg_amount=0):
        """
        This deletes a specific amount of messages.\nFor example, if I wanted to delete the 13 last messages, I'd use !delete amount 13\nThe limit for this command is 500 messages
        """
        if msg_amount == 0:  # checks if you didnt enter an amount / amount is 0
            response = ":exclamation: You must choose an amount to delete.\nSyntax: ``syn delete amount 10``"
            await ctx.bot.say(response)
            async for log in ctx.bot.logs_from(ctx.message.channel, limit=5):  # deletes the response
                if log.content == response:
                    asyncio.sleep(5)
                    await ctx.bot.delete_message(log)
        else:
            if self.bot.is_whitelisted(ctx.message.server.id, ctx.message.author.id):  # checks if allowed to delete
                await ctx.bot.delete_message(ctx.message)
                count = 0
                async for log in self.bot.logs_from(ctx.message.channel, limit=int(msg_amount)):  # loop for deletion
                    await self.bot.delete_message(log)
                    count += 1
                response = "Successfully deleted %s messages" % count
                await self.bot.say(response)
                async for log in self.bot.logs_from(ctx.message.channel, limit=5):  # deletes the response
                    if log.content == response:
                        asyncio.sleep(5)
                        await self.bot.delete_message(log)
                print("%s has deleted %s messages in %s(%s)" % (ctx.message.author.name, count, ctx.message.channel, ctx.message.server))
            else:
                response = "You're not allowed to use this command!"
                await self.bot.say(response)
                async for log in self.bot.logs_from(ctx.message.channel, limit=5):  # deletes the response
                    if log.content == response:
                        asyncio.sleep(5)
                        await self.bot.delete_message(log)
                print("%s tried to delete messages but isn't allowed." % ctx.message.author.name)

    @commands.command(pass_context=True, hidden=True)
    async def roleall(self, ctx, role: discord.Role):
        count = 0
        if ctx.bot.is_admin(ctx.message.author.id):
            for member in ctx.message.server.members:
                count += 1
                if count >= 20:
                    await asyncio.sleep(5)
                    count = 0
                await ctx.bot.add_roles(member, role)


def setup(bot):
    bot.add_cog(Utilities(bot))
