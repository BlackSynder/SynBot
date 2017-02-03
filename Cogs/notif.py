import discord

class NameNotifier:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if message.author.id == "236176083861372928":
            return
        if message.channel.id == "258330960733405184":
            msg = await self.bot.send_message(discord.Object(id="277162788894277632"), "%s\n\n<@111158853839654912>" % message.content)
    

def setup(bot):
    bot.add_cog(NameNotifier(bot))
