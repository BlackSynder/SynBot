from discord.ext import commands
import discord
import random


class DiceRoll:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, error, ctx):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.bot.send_message(ctx.message.author, 'Incorrect usage. Type `syn help` for more info.')

    async def delete_messages(self, message, author):
        async for historicMessage in self.bot.logs_from(message.channel):
            if historicMessage.author == self.bot.user:
                if (author.name in historicMessage.content) or (author.mention in historicMessage.content) or (':game_die:' in historicMessage.content):
                    await self.bot.delete_message(historicMessage)

            if historicMessage.content.startswith('syn r'):
                if author == historicMessage.author:
                    try:
                        await self.bot.delete_message(historicMessage)
                    except:
                        hi = 'hello'
    async def log_rolls(self, server, log_msg):
        if server.id == "267135631103229954":
            await self.bot.send_mesage(discord.Object(id="267436115139624970"), log_msg)
        elif server.id == "210157550044315648":
            await self.bot.send_mesage(discord.Object(id="272783366837895181"), log_msg)

    @commands.command(pass_context=True)
    async def r(self, ctx, dice: str, plus=None):
        """Rolls a dice using XdX format.
        e.g ~r 3d6"""
        if plus is None:
            plus = "+0"

        total_plus = str(plus.split("+")[1])

        result_total = 0
        result_string = ''

        try:
            dice_amount = dice.split('d')[0]
            dice_sides = dice.split('d')[1]  # .split('+')[0]
        except Exception:
            await ctx.bot.say("Format has to be in xdx %s." % ctx.message.author)
            return

        if int(dice_amount) > 50:
            await ctx.bot.say("Are you retarded? I cant roll that many dice, %s." % ctx.message.author.name)
            return

        await self.delete_messages(ctx.message, ctx.message.author)

        ctx.bot.type()
        await ctx.bot.say("─:game_die:──:game_die:──:game_die:──:game_die:──:game_die:──:game_die:──:game_die:──:game_die:─\nRolling %s d%s for %s" % (dice_amount, dice_sides, ctx.message.author.mention))
        for r in range(int(dice_amount)):
            number = random.randint(1, int(dice_sides))
            result_total = result_total + number + int(total_plus)
            if result_string == '':
                result_string += str(number)
            else:
                result_string += ', ' + str(number + int(total_plus))

        if total_plus != "0":
            result_string += ",+" + str(total_plus)

        if dice_amount == '1':

            await ctx.bot.say("  **Result:** " + result_string + "\n**Total:** " + str(
                result_total) + "\n─:game_die:──:game_die:──:game_die:──:game_die:──:game_die:──:game_die:──:game_die:──:game_die:─")
            log = "%s has rolled %s %s in %s and got %s" % (ctx.message.author.name, dice, plus, ctx.message.server, result_total)
            print("%s has rolled %s %s in %s and got %s" % (ctx.message.author.name, dice, plus, ctx.message.server, result_total))
        else:

            await ctx.bot.say("  **Result:** " + result_string + "\n**Total:** " + str(
                result_total) + "\n─:game_die:──:game_die:──:game_die:──:game_die:──:game_die:──:game_die:──:game_die:──:game_die:─")
            log = "%s has rolled %s %s in %s and got %s" % (ctx.message.author.name, dice, plus, ctx.message.server, result_total)
            print("%s has rolled %s %s in %s and got %s" % (ctx.message.author.name, dice, plus, ctx.message.server, result_total))

        await self.log_rolls(ctx.message.server, log)

    @commands.command(pass_context=True)
    async def dndroll(self, ctx):
        total = 0
        final_list = []
        while total not in range(70, 80):
            final_list = []
            for stat in range(6):
                roll_list = []
                for r in range(4):
                    roll = random.randint(1, 6)
                    roll_list.append(roll)
                roll_list.remove(min(roll_list))
                final_list.append(sum(roll_list))
            total = sum(final_list)
        await self.bot.say("Your stats are:\n{stats}\nTotal roll score: {total}".format(stats=str([x for x in final_list]), total=total))
        print("%s has rolled D&D stats in %s and got %s(%s)" % (ctx.message.author.name, ctx.message.server, str([x for x in final_list]), total))


def setup(bot):
    bot.add_cog(DiceRoll(bot))
