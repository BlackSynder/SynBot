from discord.ext.commands import Bot
import os
import asyncio
from discord.ext.commands import errors
if os.path.isfile("info.py"):
    import info


token = os.environ.get("BOT_TOKEN")
if token is None:
    token = info.bot_token
os.system("cls")
os.system("title SynBot Console")
extensions = ["botpoll", "roll", "roles", "admin", "utils", "notif"]
startup_extensions = ["Cogs." + extension for extension in extensions]


class SynBot(Bot):
    def __init__(self):
        super().__init__(command_prefix="syn ", description="Misc Bot")

    async def on_command_error(self, error, ctx):
        if isinstance(error, errors.CommandNotFound):
            msg = await ctx.bot.send_message(ctx.message.channel, ":moyai: Command was not found! Type `{}help` for more info.".format(ctx.bot.command_prefix))
            asyncio.sleep(7)
            await ctx.bot.delete_message(msg)

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

    def is_whitelisted(self, server_id, user_id):  # checks the wl file if someone can use a command
        filename = "whitelist-%s.txt" % server_id
        if not os.path.isdir("Server Configs"):
            os.mkdir("Server Configs")
        path = os.path.join("Server Configs", filename)
        if not os.path.isfile(path):
            open(path, "w").close()
        with open(path, "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith(user_id):
                    return True
                else:
                    return False

    def is_admin(self, user_id):  # checks the admin file if someone can use a command
        wl_file = open("admin.txt", "r")
        lines = wl_file.readlines()
        for line in lines:
            if line.startswith(user_id):
                return True
        wl_file.close()
        return False

SynBot().run(token)
