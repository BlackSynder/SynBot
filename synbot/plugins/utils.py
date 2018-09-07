import base64
import builtins
import inspect
import os
import random
import time
from io import BytesIO, StringIO
from traceback import format_exception

import psutil
from PIL import Image

import trio
from curious import Channel, Embed, Status
from curious.commands import Plugin, command, conditions


class Utilities(Plugin):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(bot)

    @command()
    async def ping(self, ctx):
        """Displays latency"""
        before = time.monotonic()
        msg = await ctx.channel.messages.send("Pinging... \N{TABLE TENNIS PADDLE AND BALL}")
        after = time.monotonic()
        ping = round((after - before) * 1000, 2)
        await msg.edit(new_content=f"\N{TABLE TENNIS PADDLE AND BALL} Pong! **{ping}**ms")

    @command(hidden=True)
    @conditions.is_owner()
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
            "print": print
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
            return await ctx.channel.messages.send(f"```py\n{stdout}\n{result}```")
        except:  # noqa
            try:
                exec(fmt, env)
                result = await env["e"]()
            except Exception as e:
                result = ''.join(format_exception(None, e, e.__traceback__, chain=False))
        stdout = out.getvalue()
        if stdout is not "" or result is not None:
            await ctx.channel.messages.send(f"```py\n{stdout}\n{result}```")

    @command(aliases=["join", "inv"])
    async def invite(self, ctx):
        """Sends an invite link for the bot"""
        await ctx.channel.messages.send("https://discordapp.com/oauth2/authorize/?permissions=64&scope=bot&client_id=236176083861372928")

    def ByteString(ann, ctx, arg):
        return bytes(arg, 'utf-8')

    @command()
    async def img64(self, ctx, *, b64: ByteString):
        """Converts base64 to an image"""
        f = BytesIO(base64.decodebytes(b64))
        await ctx.channel.messages.upload(f, "img.png")

    def square_color(self, hexa):
        with Image.new("RGBA", (200, 200), f"#{hexa}") as img:
            img.save('color.png')

    @command()
    async def color(self, ctx, hexa):
        """Post a pic of a given hex value."""
        async with ctx.channel.typing:
            # self.bot.loop.run_in_executor(None, self.square_color, hexa)
            await trio.run_sync_in_worker_thread(self.square_color, hexa)
            await trio.sleep(1)
        embed = Embed(title=f"Color for hex `#{hexa.upper()}`:") \
            .set_image(image_url="attachment://color.png")
        await ctx.channel.messages.upload('color.png', message_embed=embed)

    @staticmethod
    def display_time(seconds: int) -> str:  # https://github.com/Fuyukai/Jokusoramame/blob/v2/jokusoramame/utils.py#L32
        """
        Turns seconds into human readable time.
        :param seconds: The amount of seconds in total.
        :return: A string of equivalent time in human readable format.
        """
        message = ''

        intervals = (
            ('week', 604_800),  # 60 * 60 * 24 * 7
            ('day', 86_400),    # 60 * 60 * 24
            ('hour', 3_600),    # 60 * 60
            ('minute', 60),
            ('second', 1),
        )

        for name, amount in intervals:
            n, seconds = divmod(seconds, amount)

            if n == 0:
                continue

            message += f"{n} {name + 's' * (n != 1)} "

        return message.strip()

    @command()
    async def uptime(self, ctx):
        """Shows bot uptime"""
        seconds = int(time.time() - psutil.Process().create_time())
        await ctx.channel.messages.send(self.display_time(seconds))

    @command()
    async def about(self, ctx):
        """Shows bot information"""
        owner = self.bot.application_info.owner
        members = [m for g in self.bot.guilds.values() for m in g.members.values()]
        total = len(members)
        unique = len({m.id for m in members})
        online = len({m.id for m in members if m.status is Status.ONLINE})
        process = psutil.Process()
        memory = process.memory_full_info().uss / 1024**2
        cpu = process.cpu_percent() / psutil.cpu_count()
        embed = (Embed(title=f"Bot Statistics", color=0x7289DA)
                 .add_field(name="Members",
                            value=f"{total} total\n{unique} unique\n{online} online")
                 .add_field(name="Servers", value=len(self.bot.guilds))
                 .add_field(name="Hardware", value=f"CPU - {cpu:.2f}%\nRAM - {memory:.2f}MB")
                 .set_author(name=str(owner), icon_url=str(owner.avatar_url)))
        await ctx.channel.messages.send(embed=embed)

    @command(aliases=['c', 'pick'])
    async def choose(self, ctx, *, options):
        """Chooses out of options.
        Syntax: s!choose option 1 | option 2 | option 3
        """
        options = options.split("|") if "|" in options else options.split()
        await ctx.channel.messages.send(random.choice(options))

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

    @command(aliases=["makechain", "channelchain", "makemessage"])
    async def scramble(self, ctx, channel: Channel = None):
        """Generates a message based on the last 1000 messages in a specified channel
        (or the current one if none was given).
        """
        channel = channel or ctx.channel
        if channel.nsfw and not ctx.channel.nsfw:
            return await ctx.channel.messages.send("Cannot post nsfw content in non-nsfw channels.")
        async with ctx.channel.typing:
            msgs = [await m.clean_content() async for m in channel.messages.get_history(limit=1000) if not m.author.user.bot]
            if not msgs:
                return await ctx.channel.messages.send("Couldn't fetch any messages from " + channel.mention)
            msg = await trio.run_sync_in_worker_thread(self.generate_message, " ".join(msgs))
        if len(msg) >= 2000:
            await ctx.channel.messages.send("Result was too large! Posting a part of it.")
            msg = msg[:2000]
        await ctx.channel.messages.send(msg)
