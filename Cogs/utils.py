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

    @commands.command(pass_context=True)
    async def delete(self, ctx, amount=0):
        """
        A command used to mass delete messages.\nThis command deletes the last messages in the channel its invoked in. Hardcoded limit for this is 500.
        """
        if amount == 0:  # checks if you didnt enter an amount / amount is 0
            await ctx.bot.say(":exclamation: You must choose an amount to delete.\nSyntax: ``syn delete 10``", delete_after=7)
        else:
            if self.bot.is_whitelisted(ctx.message.server.id, ctx.message.author.id):  # checks if allowed to delete
                await ctx.bot.delete_message(ctx.message)
                count = await self.bot.purge_from(ctx.message.channel, limit=amount)
                await self.bot.say("Successfully deleted %s messages" % len(count), delete_after=7)
                print("%s has deleted %s messages in %s(%s)" % (ctx.message.author.name, len(count), ctx.message.channel, ctx.message.server))
            else:
                await self.bot.say("You're not allowed to use this command!", delete_after=7)
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
