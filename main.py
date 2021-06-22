import discord
from discord.ext import commands
dev_token = ''
prod_token = '
intents = discord.Intents.all()
intents.members = True

startup_extensions = ['cogs.value', 'cogs.commands', 'cogs.modmail', 'cogs.general', 'cogs.template', 'cogs.pricecheck', 'cogs.screenshot', 'cogs.currency']


# When the bot connects, load the cogs
bot = commands.Bot(command_prefix ='!', intents=intents)
bot.remove_command('help')
if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(e)

bot.run(dev_token)
