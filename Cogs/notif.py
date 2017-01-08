import discord


class NameNotifier:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if message.server == discord.Object(id="258330960733405184"):
            msg = await self.bot.send_massage(discord.Object(id="258330960733405184"), "Name Said!!")
            await self.bot.delete_message(msg)


def setup(bot):
    bot.add_cog(NameNotifier(bot))
