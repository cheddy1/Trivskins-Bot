import discord
import asyncio
from discord.ext import commands
import sys, traceback
token = ''
welcomechannel = 
guildid = 
rolesid = ''
infoid = ''
announceid = ''
tradingid = ''
intents = discord.Intents.all()
intents.members = True

startup_extensions = ['cogs.value','cogs.general','cogs.modmail','cogs.template','cogs.pricecheck','cogs.screenshot']

# When the bot connects, load the cogs
bot = commands.Bot(command_prefix ='!', intents=intents)
bot.remove_command('help')
if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(e)

# Controls the rotating status, changing every two minutes
@bot.event
async def on_ready(): 
    print("Ready")
    while True:
        await bot.change_presence(activity=discord.Game(name='!help for commands',type=3))
        await asyncio.sleep(120)
        await bot.change_presence(activity=discord.Activity(name='!dm for modmail', type=3))
        await asyncio.sleep(120)
        #await bot.change_presence(activity=discord.Activity(name='cheddydev.com', type=3))
        #await client.change_presence(activity=discord.Streaming(name="FOLLOW MY TWITCH", url="https://twitch.tv/cheddyGG", type=1))
        #await asyncio.sleep(30)

# Prior to the stable release of Discord.py 1.6, .pending was not a valid operation. However, Discord had released the feature that required the use of .pending,
# so this was made with a prerelease version, so it might need to be updated with later versions of d.py
# Once a member passes the rules check, give them roles and allow them into the server
# Runs when a user joins the server
# Also prints a welcome message in the welcome channel
@bot.event
async def on_member_update(before, after):
    if (before.pending) == True:
      if (after.pending) == False:
        role = discord.utils.get(after.guild.roles, name="Trader")
        role2 = discord.utils.get(after.guild.roles, name="↥─────《 Server Rank 》────↥")
        role3 = discord.utils.get(after.guild.roles, name="↥────《 Inventory Value 》───↥")
        role4 = discord.utils.get(after.guild.roles, name="↥──────《 Self Role 》──────↥")
        await after.add_roles(role)
        await after.add_roles(role2)
        await after.add_roles(role3)
        await after.add_roles(role4)
        guild = bot.get_guild(guildid)
        welcome = guild.get_channel(welcomechannel)
        memberCount = len([m for m in guild.members if not m.bot])
        lastCount = memberCount % 100
        if lastCount == 1:
            memberCount = str(memberCount)+"st"
        elif lastCount == 2:
            memberCount = str(memberCount)+"nd"
        elif lastCount == 3:
            memberCount = str(memberCount)+"rd"
        else:
            memberCount = str(memberCount)+"th"
        await welcome.send("Welcome, "+after.mention+", to **Trivskins Trading**!\n*You are the **"+memberCount+"** member!*\n\n__Don't forget to check out:__\n<#"+infoid+"> to learn about the server and trading.\n<#"+rolesid+"> to get some roles.\n<#"+announceid+"> to see what's going on in the server currently.\n\nIf you have any qustions or comments, open a modmail by typing **!dm** anywhere in the server.\nWe hope you enjoy the server, and have fun trading!\n**\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_**")

bot.run(token)
