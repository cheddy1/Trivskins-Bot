import discord
import asyncio
from discord.ext import commands
import sys, traceback
token = '

startup_extensions = ['cogs.value','cogs.general','cogs.modmail','cogs.template','cogs.pricecheck','cogs.screenshot']

bot = commands.Bot(command_prefix ='!')
bot.remove_command('help')
if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            pass
@bot.event
async def on_ready(): #Runs when the bot connects.
    print("Ready")
    while True:
        await bot.change_presence(activity=discord.Game(name='!help | v1.0.3',type=1))
        await asyncio.sleep(120)
        await bot.change_presence(activity=discord.Activity(name='!dm for support', type=3))
        await asyncio.sleep(120)
        #await bot.change_presence(activity=discord.Activity(name='cheddydev.com', type=3))
        #await client.change_presence(activity=discord.Streaming(name="FOLLOW MY TWITCH", url="https://twitch.tv/cheddyGG", type=1))
        #await asyncio.sleep(30)
bot.run(token)
