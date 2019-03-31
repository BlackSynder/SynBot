from discord.ext.commands import Cog


class Cancer(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ok_list = [198101180180594688, 246291440106340352]

    @Cog.listener
    async def on_member_join(self, member):
        if member.guild.id not in self.ok_list:
            return
        await member.guild.system_channel.send("yes " + member.mention)

    @Cog.listener
    async def on_member_remove(self, member):
        if member.guild.id not in self.ok_list:
            return
        await member.guild.system_channel.send("no " + member.mention)

    @Cog.listener
    async def on_guild_emojis_update(self, guild, before, after):
        if guild.id not in self.ok_list:
            return
        await guild.system_channel.send("the emojis were updated")


def setup(bot):
    bot.add_cog(Cancer(bot))
