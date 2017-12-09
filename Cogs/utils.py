import asyncio
import base64
import inspect
import os
import textwrap
import time
from io import BytesIO

import discord
import psutil
from discord.ext import commands
from PIL import Image


class Utilities:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Displays latency"""
        before = time.monotonic()
        msg = await ctx.send("Pinging... \N{TABLE TENNIS PADDLE AND BALL}")
        after = time.monotonic()
        ping = round((after - before) * 1000, 2)
        await msg.edit(content=f"\N{TABLE TENNIS PADDLE AND BALL} Pong! **{ping}**ms")

    @commands.command(hidden=True, disabled=True)
    async def setavatar(self, ctx):
        pics = os.listdir("Bot Pics")
        fmt = "Enter pic number to set:\n"
        for i, pic in enumerate(pics):
            fmt += f"[{i+1}] - {pic}\n"
        img_msg = await ctx.send(fmt)
        check = lambda m: m.author == ctx.author and m.channel == ctx.channel # noqa
        try:
            msg = await self.bot.wait_for("message", check=check, timeout=35)
        except asyncio.TimeoutError:
            await img_msg.delete()
            return await ctx.send("Timeout. Please try again later.")
        img_num = int(msg.content) - 1
        if img_num > len(pics):
            await img_msg.delete()
            return await ctx.send("This image doesnt exist!")
        img_name = pics[img_num]

        with open(img_name, "rb") as f:
            await ctx.bot.user.edit(avatar=f.read())
        await ctx.send("Changed image to " + img_name)

    @commands.command(hidden=True, aliases=["eval", "evaluate"])
    @commands.is_owner()
    async def debug(self, ctx, *, code: str):
        """Evaluates code."""
        code = code.strip('`')
        python = '```py\n{}\n```'
        result = None

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'message': ctx.message,
            'server': ctx.guild,
            'guild': ctx.guild,
            'channel': ctx.channel,
            'author': ctx.author,
            'history': await ctx.channel.history().flatten(),
            't_client': self.bot.t_client
        }

        env.update(globals())

        try:
            result = eval(code, env)
            if inspect.isawaitable(result):
                result = await result
        except Exception as e:
            await ctx.send(python.format(type(e).__name__ + ': ' + str(e)))
            return

        await ctx.send(python.format(result))

    @commands.command(name="exec", hidden=True)
    @commands.is_owner()
    async def execute(self, ctx, *, code):
        if code.startswith("```") and code.endswith("```"):
            code = code.strip("```")
            if code.startswith("py\n"):
                code = code[3:]
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'message': ctx.message,
            'server': ctx.guild,
            'guild': ctx.guild,
            'channel': ctx.channel,
            'author': ctx.author,
            'history': await ctx.channel.history().flatten(),
            't_client': self.bot.t_client
        }
        env.update(globals())
        wrapped = 'async def func():\n%s' % textwrap.indent(code, '  ')
        try:
            result = exec(wrapped, env)
            func = env['func']
            ret = await func()
            if result:
                await ctx.send(f"```{result}```")
            elif ret:
                await ctx.send(f"```{ret}```")
        except Exception as e:
            await ctx.send(f"```{type(e).__name__ + ': ' + str(e)}```")

    @commands.command(aliased=["join", "inv"])
    async def invite(self, ctx):
        """Sends an invite link for the bot"""
        await ctx.send("https://discordapp.com/oauth2/authorize/?permissions=64&scope=bot&client_id=236176083861372928")

    class ByteString(commands.Converter):
        async def convert(self, ctx, arg):
            return bytes(arg, 'utf-8')

    @commands.command()
    async def img64(self, ctx, *, b64: ByteString):
        """Converts base64 to an image"""
        f = BytesIO(base64.decodebytes(b64))
        await ctx.send(file=discord.File(f, "img.png"))

    def square_color(self, hexa):
        with Image.new("RGBA", (200, 200), f"#{hexa}") as img:
            img.save('color.png')

    @commands.command()
    async def color(self, ctx, hexa):
        """Post a pic of a given hex value."""
        async with ctx.typing():
            self.bot.loop.run_in_executor(None, self.square_color, hexa)
            await asyncio.sleep(1)
        embed = discord.Embed(title=f"Color for hex `#{hexa.upper()}`:") \
            .set_image(url="attachment://color.png")
        await ctx.send(file=discord.File('color.png'), embed=embed)

    @commands.command()
    async def about(self, ctx):
        """Shows bot information"""
        owner = self.bot.get_user(self.bot.owner_id)
        total = len(list(self.bot.get_all_members()))
        unique = len(self.bot.users)
        online = len({m.id for m in self.bot.get_all_members() if m.status is discord.Status.online})
        process = psutil.Process()
        memory = process.memory_full_info().uss / 1024**2
        cpu = process.cpu_percent() / psutil.cpu_count()
        embed = (discord.Embed(title=f"Bot Statistics", color=discord.Color.blurple())
                 .add_field(name="Members",
                            value=f"{total} total\n{unique} unique\n{online} online")
                 .add_field(name="Servers", value=len(self.bot.guilds))
                 .add_field(name="Hardware", value=f"CPU - {cpu}\nRAM - {memory}")
                 .set_author(name=str(owner), icon_url=owner.avatar_url))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Utilities(bot))
