from discord.ext import commands
import discord
import os


class EmojiRoles:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def role(self, ctx, *roles: discord.Emoji):
        if ctx.message.server.id == "208380543753125889":
            channel = ctx.message.server.get_channel("242062731820138496")
            if ctx.message.channel != channel:
                await ctx.bot.delete_message(ctx.message)
                await ctx.bot.send_message(ctx.message.author, "This command can only be used in #role_request.")
        role_dict = {}
        filename = "roles-%s.txt" % ctx.message.server.id
        path = os.path.join("Server Configs", filename)
        with open(path, "r") as f:
            for line in f:
                key_dict = line.split(" ")[0]
                val_dict = line.split(" ")[1].split("\n")[0]
                role_dict[key_dict] = val_dict
        role_list = []
        has_role = False
        entered_role = False
        for role_emoji in roles:
            for role in ctx.message.server.roles:
                if role.id == str(role_dict[role_emoji.name]):
                    if role in ctx.message.author.roles:
                        await ctx.bot.say("Youre already in %s" % role.name)
                        has_role = True
                        entered_role = True
                        continue
                    has_role = True
                    print("Added role %s to %s" % (role.name, ctx.message.author.name))
                    role_list.append(role.name)
                    await ctx.bot.add_roles(ctx.message.author, role)
            if has_role is False:
                await ctx.bot.say(":%s: does not have a role attached to it. You either entered a wrong emoji or the role is not yet added." % role_emoji.name)
        if len(role_list) == 1:
            await ctx.bot.say("Added %s as role." % role_list[0])
        elif len(role_list) > 1:
            await ctx.bot.say("Added %s as roles." % role_list)
        elif entered_role is False:
            await ctx.bot.say("You must enter at least one role emoji!")

    @commands.command(pass_context=True)
    async def getroles(self, ctx):
        """Gets a list of all roles in the server"""
        if not self.bot.is_whitelisted(ctx.message.server.id, ctx.message.author.id):
            await ctx.bot.say(":exclamation: You cannot use this command!")
            return
        response = "`Roles ID:`"
        for role in ctx.message.server.roles:
            if not role.is_everyone:
                if len(ctx.message.server.roles) > 15:
                    await ctx.bot.say(response)
                    response = "\n" + "Role name: %s ID: %s" % (role.name, role.id)
                else:
                    response += "\n" + "Role name: %s ID: %s" % (role.name, role.id)
        await ctx.bot.say(response)

    @commands.command(pass_context=True)
    async def assign(self, ctx, key: discord.Emoji, val):
        if not self.bot.is_whitelisted(ctx.message.server.id, ctx.message.author.id):
            await ctx.bot.say(":exclamation: You cannot use this command!")
            return
        string = '%s %s\n' % (key.name, val)
        filename = "roles-%s.txt" % ctx.message.server.id
        path = os.path.join("Server Configs", filename)
        with open(path, "a") as f:
            f.write(string)
        await ctx.bot.say("Successfully added :%s: as a role emoji!" % key.name)


def setup(bot):
    bot.add_cog(EmojiRoles(bot))
