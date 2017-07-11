from discord.ext import commands
import discord
import random
import re


class DiceRoll:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["rng", "r"])
    async def roll(self, ctx, rng):
        """Roll a dice.\nSupports Addition(+), Subtraction(-), Multiplication(*, x), Division(/).\nExample: s!roll 4d20+5"""
        pattern = r"((\d+)d(\d))([+\-*\/x]\d+)?"
        match = re.search(pattern, rng)
        if match:
            rolls = []
            dice_amount = int(match.group(2))
            if dice_amount > 200:
                await ctx.send(":exclamation: Thats WAAAAAAY too many dice!", delete_after=10)
            dice_type = int(match.group(3))
            try:
                # +N or -N
                math = int(match.group(4))
            except ValueError:
                # either xN, *N or /N
                if match.group(4):
                    math = None
                    math_action = match.group(4)[0]
                    math_number = int(match.group(4)[1:])
            except TypeError:
                # none, so no math
                pass
            for roll in range(dice_amount):
                rolls.append(random.randint(1, dice_type))
            total = sum(rolls)

            if match.group(4):
                if math:
                    total += math
                else:
                    if math_action == "*" or math_action == "x":
                        total *= math_number
                    else:
                        total /= math_number
            if total < 0:
                total = 0
            embed = discord.Embed(title="\N{GAME DIE} Dice Rolled! \N{GAME DIE}")
            embed.add_field(name="Dice", value=match.group(1), inline=True)
            embed.add_field(name="Results", value=rolls, inline=True)
            if match.group(4):
                embed.add_field(name="Total", value=f"{total} ({sum(rolls)})", inline=False)
            else:
                embed.add_field(name="Total", value=total, inline=False)
            await ctx.send(embed=embed)

        else:
            await ctx.send(":exclamation: Not a valid dice roll!", delete_after=10)

    @commands.command(aliases=["dndroll"])
    async def statroll(self, ctx):
        """Roll D&D stats"""
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
        await ctx.send("Your stats are:\n{stats}\nTotal roll score: {total}".format(stats=str([x for x in final_list]), total=total))


def setup(bot):
    bot.add_cog(DiceRoll(bot))
