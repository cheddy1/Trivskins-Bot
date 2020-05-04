import discord
import asyncio
from discord.ext import commands
import sys, traceback
token = '' #Discord Bot Token

startup_extensions = ['cogs.value','cogs.general','cogs.modmail','cogs.template']

bot = commands.Bot(command_prefix ='!')
bot.remove_command('help')
if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()
@bot.event
async def on_ready(): #Runs when the bot connects.
    print("Ready")
    while True:
        await bot.change_presence(activity=discord.Game(name='!help | v5.0.0',type=1))
        await asyncio.sleep(90)
        await bot.change_presence(activity=discord.Activity(name='cheddydev.com', type=3))
        #await client.change_presence(activity=discord.Streaming(name="FOLLOW MY TWITCH", url="https://twitch.tv/cheddyGG", type=1))
        await asyncio.sleep(20)
bot.run(token)
