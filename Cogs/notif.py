import discord

class NameNotifier:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if message.author.id == "236176083861372928":
            return
        if message.channel.id == "258330960733405184":
            em = discord.Embed.from_data(message.embeds[0])
            self.bot.delete_message(message)
            await self.bot.send_message(message.channel, embed=em)

def setup(bot):
    bot.add_cog(NameNotifier(bot))
