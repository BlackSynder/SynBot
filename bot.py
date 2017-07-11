from discord.ext.commands import Bot
import os
import asyncio



token = os.environ.get("BOT_TOKEN")
extensions = ["botpoll", "roll", "roles", "admin", "utils", "notif", "search"]
startup_extensions = ["Cogs." + extension for extension in extensions]


class SynBot(Bot):
    def __init__(self):
        super().__init__(command_prefix=["syn ", "s!"], description="Misc Bot")

    async def on_ready(self):
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

SynBot().run(token)
