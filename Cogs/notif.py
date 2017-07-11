import discord

class NameNotifier:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if message.author.id == "236176083861372928":
            return
        if message.channel.id == "258330960733405184":
            await message.delete()
            await message.channel.send(embed=message.embeds[0])
def setup(bot):
    bot.add_cog(NameNotifier(bot))
