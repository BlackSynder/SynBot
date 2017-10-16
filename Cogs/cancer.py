class Cancer:
    def __init__(self, bot):
        self.bot = bot
        self.ok_list = [198101180180594688, 246291440106340352]

    async def on_member_join(self, member):
        if not member.guild.id in self.ok_list:
            return
        await member.guild.system_channel.send("yes " + member.mention)




def setup(bot):
    bot.add_cog(Cancer(bot))
