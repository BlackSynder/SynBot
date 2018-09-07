from synbot import SynBot
from ruamel.yaml import YAML
yaml = YAML()

with open("config.yaml") as f:
    config = yaml.load(f)

TOKEN = config['TOKEN']

bot = SynBot(TOKEN, config=config)
bot.run()
