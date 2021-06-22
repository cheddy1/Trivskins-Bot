import discord
import asyncio
from discord.ext import commands
welcomechannel = 556874149121884160
guildid = 427956256175685634
rolesid = '557299561979183114'
infoid = '613715419026423814'
announceid = '556875713727168533'
intents = discord.Intents.all()
intents.members = True


class General(commands.Cog, name="Ad Template Checker"):
    def __init__(self, bot):
        self.bot = bot

    # Controls the rotating status, changing every two minutes
    @commands.Cog.listener()
    async def on_ready(self):
        print("Ready")
        while True:
            await self.bot.change_presence(activity=discord.Game(name='!help for commands', type=3))
            await asyncio.sleep(120)
            await self.bot.change_presence(activity=discord.Activity(name='!dm for modmail', type=3))
            await asyncio.sleep(120)
            # await bot.change_presence(activity=discord.Activity(name='cheddydev.com', type=3))
            # await client.change_presence(activity=discord.Streaming(name="FOLLOW MY TWITCH", url="https://twitch.tv/cheddyGG", type=1))
            # await asyncio.sleep(30)

    # Once a member passes the rules check, give them roles and allow them into the server
    # Runs when a user joins the server
    # Also prints a welcome message in the welcome channel
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.pending:
            if not after.pending:
                role = discord.utils.get(after.guild.roles, name="Trader")
                role2 = discord.utils.get(after.guild.roles, name="↥─────《 Server Rank 》────↥")
                role3 = discord.utils.get(after.guild.roles, name="↥────《 Inventory Value 》───↥")
                role4 = discord.utils.get(after.guild.roles, name="↥──────《 Self Role 》──────↥")
                await after.add_roles(role)
                await after.add_roles(role2)
                await after.add_roles(role3)
                await after.add_roles(role4)
                guild = self.bot.get_guild(guildid)
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


def setup(bot):
    bot.add_cog(General(bot))
