from discord.ext import commands
import strawpoll


class StrawPollMaker:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def poll(self, ctx):
        """
        Command for managing strawpolls
        """
        if ctx.invoked_subcommand is None:
            print("poll")
            await ctx.bot.say("Invalid Command. Use ``syn help`` for more info")

    @poll.command(pass_context=True)
    async def create(self, ctx, poll_title):
        api = strawpoll.API()
        stop = False
        counter = 1
        options = []
        await ctx.bot.say('Enter "finish" to submit the poll.')
        while stop is False:
            await ctx.bot.say('Enter option #%s' % counter)
            counter += 1
            option = await self.bot.wait_for_message(author=ctx.message.author)
            if option.content.lower() == "finish":
                if len(options) < 2:
                    await ctx.bot.say("You must submit at least 2 options. Do you want to cancel the poll?\nEnter `cancel` to cancel or enter the next option to continue.")
                    option = await self.bot.wait_for_message(author=ctx.message.author)
                    if option.content.lower() == "cancel":
                        return
                    else:
                        options.append(option.content)
                        continue
                stop = True
            else:
                options.append(option.content)
        poll = strawpoll.Poll(poll_title, options)
        async for log in ctx.bot.logs_from(ctx.message.channel, limit=counter*2-1):  # deletes the bot messages
            if log.author.id == "236176083861372928":
                await ctx.bot.delete_message(log)
        async for log in ctx.bot.logs_from(ctx.message.channel, limit=counter):  # deletes the user messages
            if log.author.id == ctx.message.author.id:
                await ctx.bot.delete_message(log)
        await ctx.bot.say("Poll title:%s\nOptions:\n%s\nDo you want to submit the poll?\nEnter `yes` to submit or anything else to cancel" % (poll_title, ", ".join([str(x) for x in options])))
        answer = await self.bot.wait_for_message(author=ctx.message.author)
        if answer.content.lower() == "yes":
            await api.submit_poll(poll)
            print("Created poll.\nPoll title = %s\n" % poll.title)
            await ctx.bot.say("Poll successfully created: %s" % poll.url)
        else:
            return


def setup(bot):
    bot.add_cog(StrawPollMaker(bot))
