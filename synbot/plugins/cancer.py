from curious import event
from curious.commands import Plugin


class Cancer(Plugin):
    def __init__(self, bot):
        self.bot = bot
        self.ok_list = [198101180180594688, 246291440106340352]
        super().__init__(bot)

    @event("guild_member_add")
    async def on_member_join(self, ctx, member):
        if member.guild.id not in self.ok_list:
            return
        await member.guild.system_channel.send("yes " + member.mention)

    @event("guild_member_remove")
    async def on_member_remove(self, ctx, member):
        if member.guild.id not in self.ok_list:
            return
        await member.guild.system_channel.send("no " + member.mention)

    @event("guild_emojis_update")
    async def on_guild_emojis_update(self, ctx, before, after):
        if before.id not in self.ok_list:
            return
        await before.system_channel.send("the emojis were updated")
