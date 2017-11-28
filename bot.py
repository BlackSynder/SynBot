import os

import discord
import tokage
from discord.ext import commands
from discord.ext.commands import Bot


TOKEN = os.environ.get("BOT_TOKEN")
extensions = ["roll", "roles", "utils", "search", "cancer", "myanimelist"]
startup_extensions = ["Cogs." + extension for extension in extensions]


class SynBot(Bot):
    def __init__(self):
        game = discord.Game(name="s!help | syn help", type=2)
        prefix = commands.when_mentioned_or("syn ", "s!")
        super().__init__(command_prefix=prefix, description="Misc Bot", game=game)

    async def close(self):
        await self.t_client.cleanup()
        await super().close()

    async def on_ready(self):
        self.t_client = tokage.Client()

        print('Logged in!')
        print(self.user.name)
        print(self.user.id)
        print('------')
        print("Cogs loaded:")
        for extension in startup_extensions:
            try:
                self.load_extension(str(extension))
                print('"%s" loaded successfully' % extension.split(".")[1])
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(extension, exc))
        print('------')


SynBot().run(TOKEN)
