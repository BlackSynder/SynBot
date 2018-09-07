import multio
from curious import Client, Game, event
from curious.commands import CommandsManager

multio.init('trio')

plugins = ["roll", "utils", "search", "cancer", "anilist"]
modules = ["synbot.plugins." + p for p in plugins]


class SynBot(Client):
    def __init__(self, token, *, config):
        super().__init__(token)
        self.config = config
        self.prefixes = ['tsyn ', "ts!"] if self.config['dev'] else ["syn ", 's!']
        self.manager = CommandsManager.with_client(self, command_prefix=self.prefixes)

    async def close(self):
        # await self.klient.cleanup()  # soon
        await super().close()

    @event("message_created")
    async def on_message(self, ctx, message):
        if ctx.author.user.bot:
            return
        await self.manager.handle_commands(ctx, message)

    @event("ready")
    async def on_ready(self, ctx):
        self.owner_id = 111158853839654912
        print('Logged in!')
        print(self.user.name)
        print(self.user.id)
        print('------')
        print("Plugins loaded:")
        for mod in modules:
            try:
                await self.manager.load_plugins_from(mod)
                print(mod.split(".")[-1], "loaded successfully.")
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(mod, exc))
        print('------')
        await self.change_status(game=Game(name="help | ".join(self.prefixes) + "help", type=2))
