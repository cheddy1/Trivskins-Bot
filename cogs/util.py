import discord
from discord.ext import commands

from env_secrets import get_guild_id

welcome_channel = "👀︱welcome"
roles_channel = "📌︱roles"
info_channel = "💬︱info"
announcements_channel = "📢︱announcements"


class Util(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    # Controls the rotating status, changing every two minutes
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            activity=discord.Activity(
                name="/help for commands",
                type=3,
            )
        )
        # while True:
        #
        #     await asyncio.sleep(120)
        #     await self.bot.change_presence(
        #         activity=discord.Activity(name="!dm for modmail", type=3)
        #     )
        #     await asyncio.sleep(120)
        # await bot.change_presence(activity=discord.Activity(name='cheddydev.com', type=3))
        # await client.change_presence(activity=discord.Streaming(name="FOLLOW MY TWITCH", url="https://twitch.tv/cheddyGG", type=1))
        # await asyncio.sleep(30)

    # Once a member passes the rules check, give them roles and allow them into the server
    # Runs when a user joins the server
    # Also prints a welcome message in the welcome channel
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = self.bot.get_guild(get_guild_id())
        if guild is not None:
            member_count = guild.member_count
            if member_count is not None:
                member_count_fmt = f"{member_count}" + (
                    {1: "st", 2: "nd", 3: "rd"}.get(member_count % 10, "th")
                    if member_count not in (11, 12, 13)
                    else "th"
                )
                welcome = discord.utils.get(guild.text_channels, name=welcome_channel)
                roles = discord.utils.get(guild.text_channels, name=roles_channel)
                announcements = discord.utils.get(guild.text_channels, name=announcements_channel)
                info = discord.utils.get(guild.text_channels, name=info_channel)
                channel_list = [roles, announcements, info, welcome]
                if all(channel is not None for channel in channel_list):
                    await welcome.send(
                        f"Welcome, {member.mention}, to **Trivskins Trading**!\n*You are the **{member_count_fmt}** member!*\n\n__Don't forget to check out:__\n<#{info.id}> to learn about the server and trading.\n<#{roles.id}> to get some roles.\n<#{announcements.id}> to see what's going on in the server currently.\n\nWe hope you enjoy the server, and have fun trading!\n**\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_**"
                    )


async def setup(bot):
    await bot.add_cog(Util(bot))
