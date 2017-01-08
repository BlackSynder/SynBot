import discord


class NameNotifier:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        print("msg")
        if message.author.id == "236176083861372928":
            return
        if message.channel.id == "258330960733405184":
            print("yes")
            msg = await self.bot.send_message(discord.Object(id="258330960733405184"), "<@111158853839654912>")
            await self.bot.delete_message(msg)


def setup(bot):
    bot.add_cog(NameNotifier(bot))
