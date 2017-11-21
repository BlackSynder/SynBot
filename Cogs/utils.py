import os
import asyncio
import inspect
import textwrap
import base64
from io import BytesIO

import tokage
import discord
from discord.ext import commands


class Utilities:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def setavatar(self, ctx):
        pics = os.listdir("Bot Pics")
        fmt = "Enter pic number to set:\n"
        for i, pic in enumerate(pics):
            fmt += f"[{i+1}] - {pic}\n"
        img_msg = await ctx.send(fmt)
        check = lambda m: m.author == ctx.author and m.channel == ctx.channel
        try:
            msg = await self.bot.wait_for("message", check=check, timeout=35)
        except asyncio.TimeoutError:
            await img_msg.delete()
            return await ctx.send("Timeout. Please try again later.")
        img_num = int(msg.content)-1
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
            't_client': tokage.Client()
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
            't_client': tokage.Client()
        }
        env.update(globals())
        wrapped = 'async def func():\n%s' % textwrap.indent(code, '  ')
        try:
            result = exec(wrapped, env)
            func = env['func']
            await func()
            if result:
                await ctx.send(f"```{result}```")
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

def setup(bot):
    bot.add_cog(Utilities(bot))
