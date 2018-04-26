import asyncio
import base64
import builtins
import inspect
import os
import random
import time
from io import BytesIO, StringIO
from traceback import format_exception

import discord
import psutil
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
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

    @commands.command(hidden=True)
    @commands.is_owner()
    async def eval(self, ctx, *, code):

        out = StringIO()

        def print(*args, **kwargs):
            f = kwargs.pop('file', False) or out
            builtins.print(*args, **kwargs, file=f)

        env = {
            "ctx": ctx,
            "message": ctx.message,
            "channel": ctx.channel,
            "guild": ctx.guild,
            "author": ctx.author,
            "bot": ctx.bot,
            "print": print,
            "history": await ctx.history().flatten()
        }
        env.update(globals())

        code = code.strip("`")
        code = code.replace("py\n", "")
        fmt = "async def e():\n"
        fmt += "\n".join(["    " + ln for ln in code.split("\n")])

        try:
            result = eval(code, env)
            stdout = out.getvalue()
            if inspect.isawaitable(result):
                result = await result
            return await ctx.send(f"```py\n{stdout}\n{result}```")
        except:  # noqa
            try:
                exec(fmt, env)
                result = await env["e"]()
            except Exception as e:
                result = ''.join(format_exception(None, e, e.__traceback__, chain=False))
        stdout = out.getvalue()
        if stdout is not "" or result is not None:
            await ctx.send(f"```py\n{stdout}\n{result}```")

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
                 .add_field(name="Hardware", value=f"CPU - {cpu:.2f}%\nRAM - {memory:.2f}MB")
                 .set_author(name=str(owner), icon_url=owner.avatar_url))
        await ctx.send(embed=embed)

    @commands.command(aliases=['c', 'pick'])
    async def choose(self, ctx, *, options):
        """Chooses out of options.
        Syntax: s!choose option 1 | option 2 | option 3
        """
        options = options.split("|") if "|" in options else options.split()
        await ctx.send(random.choice(options))

    def generate_message(self, messages):
        words = messages.split(' ')
        index = 1
        chain = {}
        for word in words[index:]:
            key = words[index - 1]
            if key in chain:
                chain[key].append(word)
            else:
                chain[key] = [word]
            index += 1

        word1 = random.choice(list(chain.keys()))
        message = word1.capitalize()
        count = 45
        while len(message.split(' ')) < count:
            word2 = random.choice(chain[word1])
            word1 = word2
            message += ' ' + word2

        if not message.endswith('.'):
            message += "."

        return message

    @commands.command(aliases=["makechain", "channelchain", "makemessage"])
    @cooldown(1, 120, BucketType.channel)
    async def scramble(self, ctx, channel: discord.TextChannel = None):
        """Generates a message based on the last 1000 messages in a specified channel
        (or the current one if none was given).
        """
        channel = channel or ctx.channel
        if channel.is_nsfw() and not ctx.channel.is_nsfw():
            return await ctx.send("Cannot post nsfw content in non-nsfw channels.")
        async with ctx.typing():
            msgs = [m.clean_content async for m in channel.history(limit=1000)]
            msg = await self.bot.loop.run_in_executor(None, self.generate_message, " ".join(msgs))
        if len(msg) >= 2000:
            await ctx.send("Result was too large! Posting a part of it.")
            msg = msg[:2000]
        await ctx.send(msg)


def setup(bot):
    bot.add_cog(Utilities(bot))
